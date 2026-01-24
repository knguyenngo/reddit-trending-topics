import React from "react";

interface CommentViewProps {
  topic: any;
  onDeselect: () => void;
}

const CommentView: React.FC<CommentViewProps> = ({ topic, onDeselect }) => {
  return (
    <div className="w-1/2 h-screen flex flex-col bg-black">
      {/* Header section - fixed */}
      <div className="flex-shrink-0 p-4 border-b border-gray-700">
        {/* Deselect button */}
        <button
          onClick={onDeselect}
          className="mb-2 px-2 py-1 bg-red-500 text-white rounded"
        >
          Close
        </button>
        {/* Topic header */}
        <h2 className="font-bold text-lg mb-2">
          Posts for topic: {topic.topic_id}
        </h2>
      </div>
      
      {/* Scrollable content area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {topic.posts.map((post: string, idx: number) => (
          <div
            key={idx}
            className="bg-gray-800 text-white p-3 rounded-lg shadow-md border-l-4 border-blue-500 max-w-4xl"
          >
            {post}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CommentView;
