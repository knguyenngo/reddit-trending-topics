import math
import data_utils as ut

def get_dot_product(vector_a, vector_b):
    return sum(a * b for a, b in zip(vector_a, vector_b))

def get_magnitude(vector):
    return math.sqrt(sum(x ** 2 for x in vector))

def cosine_similarity(vector_a, vector_b):
    dot_product = get_dot_product(vector_a, vector_b)    
    mag_a, mag_b = get_magnitude(vector_a), get_magnitude(vector_b)
    return dot_product / (mag_a * mag_b) if (mag_a * mag_b) > 0 else 0.0

def vectorize_posts(post_tfidf, word_types):
    # Initialize post vector
    post_vector = [0] * len(word_types)

    # Check if word appears in post then record tfidf in post vector
    for i in range(len(word_types)):
        word = word_types[i]
        if word in post_tfidf:
            post_vector[i] = post_tfidf[word]
    return post_vector

def find_similar_posts(post_id, all_post_vectors, n=5):
    # Get vector of current post
    current_post_vector = all_post_vectors[post_id]
    similar_posts = {}

    # Calculate similarity between current post and all other post vectors
    for post, vector in all_post_vectors.items():
        if post != post_id:
            similarity = cosine_similarity(current_post_vector, vector)
            similar_posts[post] = similarity

    # Return top n similar posts
    return [(post, cosine_sim) for post, cosine_sim in sorted(similar_posts.items(), key=lambda x: x[1], reverse=True)[:n]]
