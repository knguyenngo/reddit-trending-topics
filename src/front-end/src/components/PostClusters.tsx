import React from "react";
import type { CorpusAnalysis } from "../types/index.ts";

function PostClusters(props: { data: CorpusAnalysis }) {
  const clusters = Object.entries(props.data.topic_clusters)
    .map(([clusterTitle, similarPostsArray]) => ({
      clusterTitle: clusterTitle,
      postCount: similarPostsArray.length,
      keywords: similarPostsArray[0]?.top_words.slice(0, 5) || [],
      similarPosts: similarPostsArray.slice(0, 3)
    }));

  return (
    <div className="flex flex-col items-center bg-red-500 rounded-[2rem] gap-4 w-full h-[400px] overflow-y-auto scrollbar-hide p-4">
      {clusters.map((cluster) => (
        <div key={cluster.clusterTitle} className="flex flex-col gap-1 p-3 bg-black/50 hover:bg-black/80 rounded-xl transition-all cursor-pointer w-full text-white">
          <span className="truncate text-sm font-medium">{cluster.clusterTitle}</span>
          <span className="text-xs text-white/50">{cluster.postCount} posts</span>
          <span className="text-xs text-white/40 truncate">{cluster.keywords.join(", ")}</span>
        </div>
      ))}
    </div>
  );
}

export default PostClusters;
