import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

// Shape of your topic objects
interface Topic {
  topic_id: number;
  keywords: string;
  post_count: number;
  sample_content: string;
  top_words: string[];
}

// Props: BubbleChart receives an array of topics
interface BubbleChartProps {
  data: Topic[];
  onSelectTopic?: (topic: Topic) => void; // ✅ pass full topic
}

// Custom node type = Topic + D3 simulation fields
interface Node extends d3.SimulationNodeDatum, Topic {
  radius: number; // bubble radius, derived from post_count
  x: number; // x position
  y: number; // y position
}

const BubbleChart: React.FC<BubbleChartProps> = ({ data, onSelectTopic }) => {
  // Reference to the <svg> element in the DOM
  const svgRef = useRef<SVGSVGElement | null>(null);

  // State to hold tooltip info (null when hidden)
  const [tooltip, setTooltip] = useState<{
    x: number;
    y: number;
    content: string;
  } | null>(null);

  useEffect(() => {
    if (!data || data.length === 0) return;

    const width = 800; // chart width
    const height = 600; // chart height

    // Select <svg> element and set size
    const svg = d3
    .select(svgRef.current)
    .attr("width", width)
    .attr("height", height);

    // Remove anything previously drawn inside <svg>
    svg.selectAll("*").remove();

    // Scale: map post_count → bubble radius
    const radiusScale = d3
    .scaleSqrt()
    .domain([0, d3.max(data, (d) => d.post_count) || 0])
    .range([10, 80]);

    // Convert topics → simulation nodes
    const nodes: Node[] = data.map((d) => ({
      ...d,
      radius: radiusScale(d.post_count),
      x: Math.random() * width,
      y: Math.random() * height,
    }));

    // Force simulation = makes bubbles "settle" naturally
    const simulation = d3
    .forceSimulation(nodes)
    .force("x", d3.forceX(width / 2).strength(0.05))
    .force("y", d3.forceY(height / 2).strength(0.05))
    .force("collide", d3.forceCollide<Node>((d) => d.radius + 2))
    .on("tick", ticked);

    // Function called every simulation "tick"
    function ticked() {
      const u = svg.selectAll<SVGGElement, Node>("g").data(nodes);

      const g = u.enter().append("g").merge(u);

      g.selectAll("circle").remove();
      g.selectAll("text").remove();

      // Draw bubble (circle)
      g.append("circle")
        .attr("r", (d) => d.radius)
        .attr("fill", "#69b3a2")
        .attr("stroke", "black")
        .attr("stroke-width", 1)
        .on("mouseover", (event, d) => {
          setTooltip({
            x: event.pageX,
            y: event.pageY,
            content: `${d.keywords} (${d.post_count} posts)`,
          });
        })
        .on("mousemove", (event) => {
          setTooltip((prev) =>
            prev ? { ...prev, x: event.pageX, y: event.pageY } : null
          );
        })
        .on("mouseout", () => {
          setTooltip(null);
        })
        .on("click", (_, d) => {
          if (onSelectTopic) {
            onSelectTopic(d); // ✅ pass the full topic object
          }
        });

      // Add a text label inside the bubble
      g.append("text")
        .text((d) => d.topic_id.toString())
        .attr("text-anchor", "middle")
        .attr("dy", ".3em")
        .attr("font-size", "12px");

      g.attr("transform", (d) => `translate(${d.x}, ${d.y})`);
    }

    return () => {
      simulation.stop();
    };
  }, [data, onSelectTopic]);

  return (
    <div className="bg-white relative">
      {/* SVG = chart container */}
      <svg ref={svgRef}></svg>

      {/* Tooltip rendered in HTML overlay */}
      {tooltip && (
        <div
          className="absolute bg-black text-white text-sm px-2.5 py-1 border border-gray-300 rounded pointer-events-none"
          style={{
            left: tooltip.x + 2,
            top: tooltip.y + 2,
          }}
        >
          {tooltip.content}
        </div>
      )}
    </div>
  );
};

export default BubbleChart;

