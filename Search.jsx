import React, { useState, useCallback, useMemo, useEffect } from 'react';
import WordGraph from '../components/Wordgraph';
import api from '../api';

export default function Search() {
  const [word, setWord] = useState('');
  const [graphData, setGraphData] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchData = useCallback(async (query) => {
    if (!query) return;
    
    setIsLoading(true);
    try {
      console.log('Requesting URL:', process.env.REACT_APP_API_URL);
      const data = await api.searchWord(query);
      console.log('API response:', data);
  
      if (data.valid) {
        const { word, synonyms, antonyms, collocations, definition } = data;
        
        let limitedSynonyms = synonyms.slice(0, 5);
        let limitedAntonyms = antonyms.slice(0, 5);
        let limitedCollocations = collocations.slice(0, 5);
        
        // NODES-FIXED
        const centerX = 0;
        const centerY = 0;
        const radius = 150;
        
        // ASSIGN POS
        const setupNodePosition = (items, type, startAngle, endAngle) => {
          if (items.length === 0) return [];
        
          return items.map((item, idx) => {
            const sectorSize = endAngle - startAngle;
            const angle = startAngle + (idx * (sectorSize / (items.length || 1)));
            const nodeRadius = radius * (0.85 + Math.random() * 0.25); // SLIGHT RAND
        
            return {
              id: item,
              type: type,
              x: centerX + nodeRadius * Math.cos(angle),
              y: centerY + nodeRadius * Math.sin(angle),
            };
          });
        };
        
        const nodes = [
          { id: word, type: 'main', x: centerX, y: centerY },
          ...setupNodePosition(limitedSynonyms, 'synonym', 0, 2 * Math.PI / 3),
          ...setupNodePosition(limitedAntonyms, 'antonym', 2 * Math.PI / 3, 4 * Math.PI / 3),
          ...setupNodePosition(limitedCollocations, 'collocation', 4 * Math.PI / 3, 2 * Math.PI),
        ];
        
        const links = [
          ...limitedSynonyms.map(s => ({ source: word, target: s, relation: 'synonym' })),
          ...limitedAntonyms.map(a => ({ source: word, target: a, relation: 'antonym' })),
          ...limitedCollocations.map(c => ({ source: word, target: c, relation: 'collocation' })),
        ];
        
        setGraphData({ nodes, links });
        setError(null);
      } else {
        setError({ error: data.error || 'Invalid data received', suggestion: data.suggestion });
        setGraphData(null);
      }
    } catch (e) {
      const errorDetails = e.response
        ? JSON.stringify(e.response.data, null, 2)
        : e.message;
      console.error('Error during API request:', e, 'Details:', errorDetails);
      setError({ error: 'API request failed', details: errorDetails });
      setGraphData(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleSearch = useCallback(() => {
    if (word.trim()) {
      fetchData(word.trim());
    }
  }, [word, fetchData]);

  const [nodeDefinition, setNodeDefinition] = useState('');
  // SETUP FOR DEFINITIONS

  const handleNodeClick = useCallback((node) => {
    setWord(node.id);
    fetchData(node.id);
    
    // FETCH DEFINITION OF CLICKED NODE
    const nodeData = graphData.nodes.find(n => n.id === node.id);
  if (nodeData) {
    setNodeDefinition(nodeData.definition || "No definition available.");
  }
}, [graphData, fetchData]);

  // ENTERSPACE HANDLER
  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  }, [handleSearch]);

  // MEMOIZE FOR PERFORMANCE
  const graphComponent = useMemo(() => {
    if (!graphData) return null;
    return <WordGraph graphData={graphData} onNodeClick={handleNodeClick} />;
  }, [graphData, handleNodeClick]);

  return (
    <div className="min-h-screen flex justify-center items-center bg-white text-gray-800 px-4 py-10">
      <div className="max-w-3xl w-full mx-4 bg-white shadow-lg rounded-lg p-8">
        <h2 className="text-2xl font-semibold mb-6 text-center">Search Word Relationships</h2>
  
        <div className="flex gap-2 mb-4 justify-center">
          <input
            value={word}
            onChange={(e) => setWord(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter a word..."
            className="flex-1 px-4 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSearch}
            className={`${
              isLoading ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'
            } text-white px-6 py-2 rounded-lg transition`}
            disabled={isLoading}
          >
            {isLoading ? 'Loading...' : 'Search'}
          </button>
        </div>
  
        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
            {error.error}
            {error.suggestion && <span> (Did you mean: <strong>{error.suggestion}</strong>?)</span>}
            {error.details && <pre className="mt-2 text-sm">{error.details}</pre>}
          </div>
        )}
  
        {graphData && (
          <div className="mt-8">
            {graphComponent}
          </div>
        )}
  
        {/* NODE-DEFINITION DISPLAY */}
        {nodeDefinition && (
          <div className="mt-4 p-4 border-t border-gray-300">
            <h3 className="text-xl font-semibold">Definition</h3>
            <p className="text-gray-700">{nodeDefinition}</p>
          </div>
        )}
      </div>
    </div>
  );
}