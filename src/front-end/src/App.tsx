import { useEffect, useState } from 'react';
import { fetchCorpusAnalysis } from './utils/dataLoader';
import type { CorpusAnalysis } from './types';
import CorpusStats from './components/CorpusStats';
import './App.css';

function App() {
  const [corpusData, setCorpusData] = useState<CorpusAnalysis | null>(null);

  useEffect(() => {
    fetchCorpusAnalysis('GlobalOffensive')
      .then(setCorpusData)
      .catch(console.error);
  }, []);

  if (!corpusData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex flex-row h-screen">
      <div className="w-64 bg-white">
      </div>
      <div className="flex flex-col flex-1">
        <div className="h-20 bg-red-500"></div>
        <div className="flex-1 bg-gray-500 grid grid-cols-2 grid-rows-2 gap-4 p-6">
          <CorpusStats data={corpusData}/>
          <div className="bg-white"></div>
          <div className="bg-white"></div>
          <div className="bg-white"></div>
        </div>
      </div>
    </div>
  );
}

export default App;
