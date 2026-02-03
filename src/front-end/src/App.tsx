import { useEffect, useState } from 'react';
import { fetchCorpusAnalysis } from './utils/dataLoader';
import type { CorpusAnalysis } from './types';
import CorpusStats from './components/CorpusStats';

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

  return <CorpusStats data={corpusData} />;
}

export default App;
