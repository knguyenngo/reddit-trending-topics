import React from "react";
import type { CorpusAnalysis } from "../types/index.ts"

function TopPosts(props: { data : CorpusAnalysis}) {
  // Convert data into object for Recharts
  const topPosts = Object.entries(props.data.top_engaged_posts)
  .map(([id, postObject]) => ({
    post_title: postObject.title,
    comments: postObject.comment_count
  }))
  .sort((a, b) => b.comments - a.comments) // Sort by comment count

  return (
    <div className="flex flex-col items-center bg-red-500 rounded-[2rem] gap-4 w-full h-[400px] overflow-y-auto scrollbar-hide p-4">
      {
        topPosts
        .map((post) => (
          <div key={post.post_title} className="flex items-center justify-between p-3 bg-black/50 hover:bg-black/80 rounded-xl transition-all cursor-pointer w-full text-white">
            <span className="truncate pr-4 text-sm font-medium">{post.post_title}</span>
            <span className="text-xs bg-red-500 px-2 py-1 rounded-full">{post.comments}</span>
          </div>
        ))
      }
    </div>
  );
}

export default TopPosts;
