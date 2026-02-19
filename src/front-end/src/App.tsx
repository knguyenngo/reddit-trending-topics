import { useEffect, useState } from 'react';
import { fetchCorpusAnalysis, fetchUnigrams } from './utils/dataLoader';
import type { CorpusAnalysis, UnigramFrequency } from './types';
import CorpusStats from './components/CorpusStats';
import FrequencyChart from './components/FrequencyChart';
import TopPosts from './components/TopPosts';
import PostClusters from './components/PostClusters';
import './App.css';

function App() {
  const [corpusData, setCorpusData] = useState<CorpusAnalysis | null>(null);
  const [unigramData, setUnigramData] = useState<UnigramFrequency | null>(null);

  // Fetch necessary data to display
  useEffect(() => {
    Promise.all([
      fetchUnigrams('GlobalOffensive'),
      fetchCorpusAnalysis('GlobalOffensive')
    ])
      .then(([unigrams, corpus]) => {
        setUnigramData(unigrams);
        setCorpusData(corpus);
      })
      .catch(console.error);
  }, []);

  if (!corpusData || !unigramData) {
    return <div>Loading...</div>;
  }

  // Our main app
  return (
    <div className="flex flex-row h-screen">
      <div className="w-64 bg-white">
      </div>
      <div className="flex flex-col flex-1">
        <div className="h-20 bg-red-500"></div>
        <div className="flex-1 bg-gray-500 grid grid-cols-2 grid-rows-2 gap-4 p-6">
          <CorpusStats data={corpusData}/>
          <FrequencyChart data={unigramData}/>
          <TopPosts data={corpusData}/>
          <PostClusters data={corpusData}/>
        </div>
      </div>
    </div>
  );
}

export default App;
