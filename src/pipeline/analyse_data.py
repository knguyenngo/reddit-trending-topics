import json
import re
import os
from pathlib import Path
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime, timedelta

# Get the project root directory (2 levels up from this script)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent.parent

COMMENT_DIR = PROJECT_DIR / "data" / "raw" / "post_comments"
RAW_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_DIR = PROJECT_DIR / "data" / "clean"

def load_posts_metadata():
    """Load original posts data for context"""
    raw_dir = Path(RAW_DIR)
    
    # Look for posts file (starts with "posts_")
    for file_path in raw_dir.glob("posts_*.json"):
        try:
            with open(file_path, 'r') as f:
                print(f"Loading posts from: {file_path.name}")
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue
    
    print("No posts file found in raw directory")
    return {}

def load_all_comments():
    """Load all comments with post metadata"""
    all_comments = []
    post_stats = defaultdict(lambda: {'comments': [], 'total_length': 0})
    
    comment_dir = Path(COMMENT_DIR)
    for file_path in comment_dir.glob("*.json"):
        try:
            with open(file_path, 'r') as f:
                comments = json.load(f)
                
            post_id = file_path.stem.split('_')[0]
            
            for comment in comments:
                if comment and comment.strip() not in ['[deleted]', '[removed]']:
                    all_comments.append({
                        'text': comment,
                        'post_id': post_id,
                        'length': len(comment)
                    })
                    post_stats[post_id]['comments'].append(comment)
                    post_stats[post_id]['total_length'] += len(comment)
                    
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return all_comments, dict(post_stats)

def advanced_cleaning(comments):
    """More sophisticated cleaning with MMA-specific filtering"""
    cleaned = []
    patterns = {
        'questions': r'\?',
        'exclamations': r'!',
        'mentions': r'(@\w+|/u/\w+)',
        'urls': r'http\S+|www\S+',
        'quotes': r'&gt;.*?(?=\n|$)',
        'edits': r'(edit:|edited:|update:)',
    }
    
    # MMA-specific stop words to filter out obvious terms
    mma_stop_words = {
        'fight', 'fighter', 'fighting', 'ufc', 'mma', 'mixed', 'martial', 'arts',
        'round', 'rounds', 'win', 'loss', 'match', 'bout', 'card', 'event'
    }
    
    for comment_data in comments:
        text = comment_data['text']
        
        if len(text.strip()) < 25:
            continue
            
        # Track comment characteristics
        characteristics = {}
        for pattern_name, pattern in patterns.items():
            characteristics[pattern_name] = len(re.findall(pattern, text, re.IGNORECASE))
        
        # Clean text
        clean_text = text
        clean_text = re.sub(patterns['urls'], '', clean_text)
        clean_text = re.sub(patterns['mentions'], '', clean_text)
        clean_text = re.sub(patterns['quotes'], '', clean_text)
        clean_text = re.sub(r'[^\w\s.,!?\'"-]', ' ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        if len(clean_text) > 20:
            cleaned.append({
                'text': clean_text,
                'original_text': text,
                'post_id': comment_data['post_id'],
                'length': len(clean_text),
                'characteristics': characteristics,
                'mma_stop_words': mma_stop_words  # Pass along for later use
            })
    
    return cleaned

def extract_controversial_topics(comments, threshold=0.3):
    """Find topics that generate debate (lots of back-and-forth)"""
    # Group by post
    post_discussions = defaultdict(list)
    for comment in comments:
        post_discussions[comment['post_id']].append(comment['text'])
    
    controversial = []
    for post_id, post_comments in post_discussions.items():
        if len(post_comments) < 5:
            continue
            
        # Use TF-IDF to find common themes in this post
        vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform(post_comments)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get most discussed terms
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            top_indices = mean_scores.argsort()[-5:][::-1]
            hot_topics = [feature_names[i] for i in top_indices]
            
            controversial.append({
                'post_id': post_id,
                'comment_count': len(post_comments),
                'hot_keywords': hot_topics,
                'avg_comment_length': np.mean([len(c) for c in post_comments])
            })
        except:
            continue
    
    return sorted(controversial, key=lambda x: x['comment_count'], reverse=True)

def analyze_discussion_patterns(comments):
    """Analyze how people discuss topics"""
    patterns = {
        'agreement_words': ['agree', 'exactly', 'this', 'yes', 'right', 'correct', 'true'],
        'disagreement_words': ['wrong', 'disagree', 'no', 'but', 'however', 'actually', 'nope'],
        'uncertainty_words': ['maybe', 'probably', 'might', 'could', 'perhaps', 'unsure'],
        'strong_words': ['definitely', 'absolutely', 'never', 'always', 'completely', 'totally'],
        'question_words': ['why', 'how', 'what', 'when', 'where', 'who'],
    }
    
    discussion_stats = defaultdict(int)
    
    for comment in comments:
        text_lower = comment['text'].lower()
        
        for pattern_type, words in patterns.items():
            if any(word in text_lower for word in words):
                discussion_stats[pattern_type] += 1
        
        # Check for other patterns
        if len(comment['text']) > 200:
            discussion_stats['long_form'] += 1
        if comment['characteristics']['questions'] > 0:
            discussion_stats['asks_questions'] += 1
        if comment['characteristics']['exclamations'] > 2:
            discussion_stats['emotional'] += 1
    
    return dict(discussion_stats)

def find_recurring_themes(comments, min_posts=3):
    """Find themes that appear across multiple posts"""
    # Group comments by post
    post_groups = defaultdict(list)
    for comment in comments:
        post_groups[comment['post_id']].append(comment['text'])
    
    # Extract keywords from each post
    post_keywords = {}
    for post_id, post_comments in post_groups.items():
        if len(post_comments) < 3:
            continue
            
        try:
            vectorizer = TfidfVectorizer(max_features=20, stop_words='english', ngram_range=(1,2))
            tfidf_matrix = vectorizer.fit_transform(post_comments)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get top keywords for this post
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            top_indices = mean_scores.argsort()[-10:][::-1]
            post_keywords[post_id] = [feature_names[i] for i in top_indices]
        except:
            continue
    
    # Find keywords that appear in multiple posts
    keyword_posts = defaultdict(list)
    for post_id, keywords in post_keywords.items():
        for keyword in keywords:
            keyword_posts[keyword].append(post_id)
    
    # Return recurring themes
    recurring = []
    for keyword, posts in keyword_posts.items():
        if len(posts) >= min_posts:
            recurring.append({
                'theme': keyword,
                'appears_in_posts': len(posts),
                'posts': posts
            })
    
    return sorted(recurring, key=lambda x: x['appears_in_posts'], reverse=True)

def identify_community_opinions(comments):
    """Extract what the community thinks about different topics"""
    # Advanced topic modeling with MMA-specific improvements
    texts = [c['text'] for c in comments if len(c['text']) > 30]
    
    if len(texts) < 30:
        return []
    
    # Custom stop words for MMA context
    mma_stop_words = [
        'fight', 'fighter', 'fighting', 'ufc', 'mma', 'mixed', 'martial', 'arts',
        'round', 'rounds', 'win', 'loss', 'match', 'bout', 'card', 'event', 'dana',
        'octagon', 'cage', 'ppv', 'main', 'title', 'belt', 'champion', 'championship',
        'decision', 'submission', 'knockout', 'ko', 'tko', 'ref', 'referee'
    ]
    
    # Combine with standard English stop words
    stop_words = list(set(mma_stop_words + ['english']))
    
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words=stop_words,
        min_df=4,  # More restrictive
        max_df=0.6,  # More restrictive 
        ngram_range=(1, 3)  # Include trigrams for better context
    )
    
    doc_term_matrix = vectorizer.fit_transform(texts)
    
    # Use more topics for granular insights
    n_topics = min(15, len(texts) // 15)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42, max_iter=20)
    lda.fit(doc_term_matrix)
    
    topic_assignments = lda.transform(doc_term_matrix).argmax(axis=1)
    feature_names = vectorizer.get_feature_names_out()
    
    opinions = []
    for topic_idx, topic in enumerate(lda.components_):
        # Get comments for this topic
        topic_comments = [comments[i] for i, t in enumerate(topic_assignments) if t == topic_idx]
        
        if len(topic_comments) < 5:
            continue
            
        # Extract topic keywords
        top_words_idx = topic.argsort()[-10:][::-1]
        keywords = [feature_names[i] for i in top_words_idx]
        
        # Analyze sentiment and characteristics of these comments
        topic_texts = [c['text'] for c in topic_comments]
        avg_length = np.mean([len(t) for t in topic_texts])
        
        # Find representative quotes
        representative_quotes = sorted(topic_comments, 
                                     key=lambda x: len(x['text']), 
                                     reverse=True)[:2]
        
        # Filter out obvious MMA terms from keywords for more interesting insights
        filtered_keywords = [kw for kw in keywords if not any(stop in kw.lower() for stop in mma_stop_words)]
        
        # If we filtered too much, keep some original keywords
        if len(filtered_keywords) < 3:
            filtered_keywords = keywords[:5]
        
        opinions.append({
            'topic': ' | '.join(filtered_keywords[:4]),
            'keywords': filtered_keywords[:8],
            'comment_count': len(topic_comments),
            'avg_comment_length': int(avg_length),
            'posts_involved': len(set(c['post_id'] for c in topic_comments)),
            'representative_quotes': [q['text'][:200] + '...' for q in representative_quotes],
            'discussion_intensity': 'high' if avg_length > 100 else 'medium' if avg_length > 50 else 'low'
        })
    
    return sorted(opinions, key=lambda x: x['comment_count'], reverse=True)

def generate_insights_summary(comments, post_stats, posts_metadata, controversial, patterns, recurring, opinions):
    """Generate comprehensive insights"""
    total_comments = len(comments)
    total_posts = len(post_stats)
    
    # Calculate engagement metrics
    comments_per_post = total_comments / total_posts if total_posts > 0 else 0
    avg_comment_length = np.mean([c['length'] for c in comments])
    
    # Find most active posts
    most_active_posts = sorted(
        [(pid, len(stats['comments'])) for pid, stats in post_stats.items()],
        key=lambda x: x[1], reverse=True
    )[:5]
    
    summary = {
        'meta': {
            'analysis_date': datetime.now().isoformat(),
            'total_comments': total_comments,
            'total_posts': total_posts,
            'avg_comments_per_post': round(comments_per_post, 1),
            'avg_comment_length': round(avg_comment_length, 1)
        },
        
        'engagement_insights': {
            'most_active_posts': [{'post_id': pid, 'comments': count} for pid, count in most_active_posts],
            'discussion_patterns': patterns,
            'engagement_level': 'high' if comments_per_post > 20 else 'medium' if comments_per_post > 10 else 'low'
        },
        
        'community_opinions': opinions[:8],  # Top 8 opinions
        
        'controversial_topics': controversial[:5],  # Most discussed posts
        
        'recurring_themes': recurring[:10],  # Themes across multiple posts
        
        'key_insights': []
    }
    
    # Generate key insights
    if opinions:
        top_opinion = opinions[0]
        summary['key_insights'].append(f"Most discussed topic: {top_opinion['topic']} ({top_opinion['comment_count']} comments across {top_opinion['posts_involved']} posts)")
    
    if controversial:
        summary['key_insights'].append(f"Most controversial post generated {controversial[0]['comment_count']} comments")
    
    if patterns.get('disagreement_words', 0) > patterns.get('agreement_words', 0):
        summary['key_insights'].append("Community shows more disagreement than agreement in discussions")
    elif patterns.get('agreement_words', 0) > patterns.get('disagreement_words', 0):
        summary['key_insights'].append("Community shows more agreement in discussions")
    
    if patterns.get('asks_questions', 0) > total_comments * 0.2:
        summary['key_insights'].append("Community is question-heavy - lots of seeking information/clarification")
    
    if recurring:
        summary['key_insights'].append(f"'{recurring[0]['theme']}' is a recurring theme across {recurring[0]['appears_in_posts']} different posts")
    
    return summary

def main():
    print("Loading comments and metadata...")
    all_comments, post_stats = load_all_comments()
    posts_metadata = load_posts_metadata()
    
    print(f"Loaded {len(all_comments)} comments from {len(post_stats)} posts")
    
    if len(all_comments) < 50:
        print("Not enough comments for meaningful analysis!")
        return
    
    print("Cleaning and analyzing comments...")
    cleaned_comments = advanced_cleaning(all_comments)
    print(f"After cleaning: {len(cleaned_comments)} comments")
    
    print("Finding controversial topics...")
    controversial = extract_controversial_topics(cleaned_comments)
    
    print("Analyzing discussion patterns...")
    patterns = analyze_discussion_patterns(cleaned_comments)
    
    print("Finding recurring themes...")
    recurring = find_recurring_themes(cleaned_comments)
    
    print("Extracting community opinions...")
    opinions = identify_community_opinions(cleaned_comments)
    
    print("Generating insights...")
    summary = generate_insights_summary(
        cleaned_comments, post_stats, posts_metadata, 
        controversial, patterns, recurring, opinions
    )
    
    # Save results
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)

    time_analyzed = datetime.now().isoformat()
    file_name = output_path / f"analysis_{time_analyzed}.json" 

    with open(file_name, "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print overview
    print("\n" + "="*60)
    print("DEEP SUBREDDIT ANALYSIS")
    print("="*60)
    print(f"📊 {summary['meta']['total_comments']} comments from {summary['meta']['total_posts']} posts")
    print(f"💬 {summary['meta']['avg_comments_per_post']} avg comments/post")
    print(f"📝 {summary['meta']['avg_comment_length']} avg comment length")
    
    print(f"\n🔥 ENGAGEMENT: {summary['engagement_insights']['engagement_level'].upper()}")
    
    print(f"\n💭 TOP COMMUNITY OPINIONS:")
    for i, opinion in enumerate(summary['community_opinions'][:3], 1):
        print(f"{i}. {opinion['topic']} ({opinion['comment_count']} comments, {opinion['discussion_intensity']} intensity)")
    
    print(f"\n🔄 RECURRING THEMES:")
    for theme in summary['recurring_themes'][:3]:
        print(f"• '{theme['theme']}' appears in {theme['appears_in_posts']} posts")
    
    print(f"\n🎯 KEY INSIGHTS:")
    for insight in summary['key_insights']:
        print(f"• {insight}")
    
    print(f"\n💾 Full analysis saved to: {file_name}")

if __name__ == "__main__":
    main()
