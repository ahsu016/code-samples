import React, { useRef, useEffect, useState, useCallback, memo } from 'react';
import { ForceGraph2D } from 'react-force-graph';

const WordGraph = memo(({ graphData, onNodeClick, wordDefinition }) => {
  const graphRef = useRef();
  const containerRef = useRef();

  const getDimensions = useCallback(() => {
    if (!containerRef.current) return { width: 800, height: window.innerHeight * 0.6 };
    
    return {
      width: containerRef.current.offsetWidth - 32,
      height: window.innerHeight * 0.6,
    };
  }, []);

  const [dimensions, setDimensions] = useState(getDimensions());

  // RESIZE LISTENER
  useEffect(() => {
    let timeoutId;
    const handleResize = () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => setDimensions(getDimensions()), 100);
    };
    
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      clearTimeout(timeoutId);
    };
  }, [getDimensions]);

  // OPTIMIZE-MEMOIZE
  const memoizedData = React.useMemo(() => {
    if (!graphData) return { nodes: [], links: [] };
    return graphData;
  }, [graphData]);

  // ZOOM ADJUST
  useEffect(() => {
    if (graphRef.current && graphData && graphData.nodes.length > 0) {
      const timer = setTimeout(() => {
        const mainNode = graphData.nodes.find((node) => node.type === 'main');
        if (mainNode) {
          graphRef.current.centerAt(mainNode.x, mainNode.y, 300);
          const zoomLevel = Math.max(0.7, Math.min(1.5, 15 / (graphData.nodes.length - 1)));
          graphRef.current.zoom(zoomLevel, 300);
        }
      }, 300);
      
      return () => clearTimeout(timer);
    }
  }, [graphData]);

  const nodeCanvasObject = useCallback((node, ctx, globalScale) => {
    const label = node.id;
    const fontSize = 14 / globalScale;
    ctx.font = `${fontSize}px Sans-Serif`;
    
    ctx.fillStyle = 
      node.type === 'main' ? '#ff4500' :
      node.type === 'synonym' ? '#1e90ff' :
      node.type === 'antonym' ? '#ff0000' :
      node.type === 'collocation' ? '#8a2be2' :
      '#32cd32'; // DEFAULT

    const nodeSize = 
      node.type === 'main' ? 10 : 
      node.type === 'synonym' ? 7 :
      node.type === 'antonym' ? 7 :
      node.type === 'collocation' ? 6 :
      5; // DEFAULT
    
    ctx.beginPath();
    ctx.arc(node.x, node.y, nodeSize, 0, 2 * Math.PI, false);
    ctx.fill();
    
    // LABEL DRAW
    if (globalScale > 0.4) {
      ctx.fillStyle = '#374151';
      ctx.fillText(label, node.x + 14, node.y + 5);
    }
  }, []);

  // NODE CLICK HANDLER
  const handleNodeClick = useCallback((node) => {
    if (node && onNodeClick) {
      onNodeClick(node.id);
    }
  }, [onNodeClick]);

  if (!graphData) return null;

  return (
    <div 
      ref={containerRef} 
      className="graph-container h-[60vh] w-full border rounded-lg shadow-sm p-4 bg-white"
    >
      <ForceGraph2D
        key={`${dimensions.width}-${dimensions.height}`}
        ref={graphRef}
        graphData={memoizedData}
        nodeId="id"
        nodeCanvasObject={nodeCanvasObject}
        nodeAutoColorBy={null}
        linkColor={() => '#999'}
        linkOpacity={0.6}
        width={dimensions.width}
        height={dimensions.height}
        cooldownTicks={100}
        cooldownTime={1000}
        d3AlphaDecay={0.02}
        d3VelocityDecay={0.3}
        onNodeClick={handleNodeClick}
        linkDirectionalParticles={0}
      />
    </div>
  );
});

export default WordGraph;
