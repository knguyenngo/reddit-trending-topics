import React, { useState } from "react";
import topics from "../../data/clean/topics.json";
import BubbleChart from "./components/BubbleChart";
import NavBar from "./components/NavBar.tsx";
import CommentView from "./components/CommentView.tsx";
import "./styles/App.css";

function App() {
  const [selectedTopic, setSelectedTopic] = useState<any | null>(null);

  const handleSelectTopic = (topic: any) => {
    setSelectedTopic(topic);
  };

  const handleDeselectTopic = () => {
    setSelectedTopic(null);
  };

  return (
    <div className="h-screen flex flex-col">
      <NavBar />
      <h1 className="flex justify-center text-2xl font-medium mb-4">
        Topic Bubble Chart
      </h1>

      <div className="flex flex-1 w-full bg-gray-300">
        {/* Chart container */}
        <div
          className={`flex justify-center transition-all duration-300 ${
selectedTopic ? "w-1/2" : "w-full"
}`}
        >
          <BubbleChart data={topics} onSelectTopic={handleSelectTopic} />
        </div>

        {/* Comment panel (only if a topic is selected) */}
        {selectedTopic && (
          <CommentView
            topic={selectedTopic}
            onDeselect={handleDeselectTopic}
          />
        )}
      </div>
    </div>
  );
}

export default App;

