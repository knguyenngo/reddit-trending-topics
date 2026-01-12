import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

interface Topic {
  topic: string; // Matches JSON "topic"
  keywords: string[];
  comment_count: number; // Matches JSON "comment_count"
  representative_quotes: string[];
  discussion_intensity: string;
}

interface BubbleChartProps {
  data: Topic[];
  onSelectTopic?: (topic: Topic) => void;
}

interface Node extends d3.SimulationNodeDatum, Topic {
  radius: number;
  x: number;
  y: number;
  color: string;
}

const BubbleChart: React.FC<BubbleChartProps> = ({ data, onSelectTopic }) => {
  const svgRef = useRef<SVGSVGElement | null>(null);

  const [tooltip, setTooltip] = useState<{
    x: number;
    y: number;
    content: string;
  } | null>(null);

  useEffect(() => {
    if (!data || !Array.isArray(data) || data.length === 0) return;

    const width = 800;
    const height = 600;

    const svg = d3
      .select(svgRef.current)
      .attr("width", width)
      .attr("height", height);

    svg.selectAll("*").remove();

    const radiusScale = d3
      .scaleSqrt()
      .domain([0, d3.max(data, (d) => d.comment_count) || 0])
      .range([20, 100]);

    const makeUniqueColors = (n: number) => {
      const colors: string[] = [];
      for (let i = 0; i < n; i++) {
        const hue = Math.floor((360 / n) * i);
        colors.push(`hsl(${hue}, 70%, 60%)`);
      }
      return d3.shuffle(colors);
    };

    const colors = makeUniqueColors(data.length);

    const nodes: Node[] = data.map((d, i) => ({
      ...d,
      radius: radiusScale(d.comment_count),
      x: Math.random() * width,
      y: Math.random() * height,
      color: colors[i],
    }));

    const nodeGroups = svg
      .selectAll<SVGGElement, Node>("g")
      .data(nodes)
      .enter()
      .append("g")
      .style("cursor", "pointer")
      .on("click", (_, d) => {
        if (onSelectTopic) onSelectTopic(d);
      });

    nodeGroups
      .append("circle")
      .attr("r", (d) => d.radius)
      .attr("fill", (d) => d.color)
      .attr("stroke", "white")
      .attr("stroke-width", 2)
      .on("mouseover", (event, d) => {
        setTooltip({
          x: event.pageX,
          y: event.pageY,
          content: `${d.topic.split('|')[0]} (${d.comment_count} comments)`,
        });
      })
      .on("mousemove", (event) => {
        setTooltip((prev) =>
          prev ? { ...prev, x: event.pageX, y: event.pageY } : null
        );
      })
      .on("mouseout", () => setTooltip(null));

    nodeGroups
      .append("text")
      // Use slice or logic to show the first keyword if topic string is too long
      .text((d) => (d.topic ? d.topic.split(' | ')[0] : "N/A"))
      .attr("text-anchor", "middle")
      .attr("dy", ".3em")
      .attr("fill", "black")
      .attr("font-weight", "bold")
      .style("font-size", (d) => Math.min(d.radius / 3, 14) + "px")
      .style("pointer-events", "none");

    const simulation = d3
      .forceSimulation<Node>(nodes)
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("charge", d3.forceManyBody().strength(5))
      .force("collide", d3.forceCollide<Node>((d) => d.radius + 5))
      .on("tick", () => {
        nodeGroups.attr("transform", (d) => `translate(${d.x}, ${d.y})`);
      });

    return () => {
      simulation.stop();
    };
  }, [data, onSelectTopic]);

  return (
    <div className="bg-black relative inline-block border border-gray-800 rounded-lg">
      <svg ref={svgRef}></svg>
      {tooltip && (
        <div
          className="absolute bg-white text-black text-xs font-bold px-2 py-1 border rounded shadow-lg pointer-events-none z-50"
          style={{ 
            left: tooltip.x + 10, 
            top: tooltip.y - 10,
            position: 'fixed',
            transform: 'translate(0, -100%)'
          }}
        >
          {tooltip.content}
        </div>
      )}
    </div>
  );
};

export default BubbleChart;
