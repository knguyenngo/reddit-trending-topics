// BubbleChart.tsx
import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

interface Topic {
  topic_id: number;
  keywords: string;
  post_count: number;
  sample_content: string;
  top_words: string[];
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
    if (!data || data.length === 0) return;

    const width = 800;
    const height = 600;

    const svg = d3
      .select(svgRef.current)
      .attr("width", width)
      .attr("height", height);

    svg.selectAll("*").remove();

    const radiusScale = d3
      .scaleSqrt()
      .domain([0, d3.max(data, (d) => d.post_count) || 0])
      .range([10, 80]);

    // ✅ Generate unique colors (evenly spaced hues)
    const makeUniqueColors = (n: number) => {
      const colors: string[] = [];
      for (let i = 0; i < n; i++) {
        const hue = Math.floor((360 / n) * i); // evenly spaced hue
        colors.push(`hsl(${hue}, 70%, 60%)`);
      }
      // Shuffle colors so they don’t look sequential
      return d3.shuffle(colors);
    };

    const colors = makeUniqueColors(data.length);

    const nodes: Node[] = data.map((d, i) => ({
      ...d,
      radius: radiusScale(d.post_count),
      x: Math.random() * width,
      y: Math.random() * height,
      color: colors[i], // ✅ unique color
    }));

    const simulation = d3
      .forceSimulation(nodes)
      .force("x", d3.forceX(width / 2).strength(0.05))
      .force("y", d3.forceY(height / 2).strength(0.05))
      .force("collide", d3.forceCollide<Node>((d) => d.radius + 2))
      .on("tick", ticked);

    function ticked() {
      const u = svg.selectAll<SVGGElement, Node>("g").data(nodes);

      const g = u.enter().append("g").merge(u);

      g.selectAll("circle").remove();
      g.selectAll("text").remove();

      g.append("circle")
        .attr("r", (d) => d.radius)
        .attr("fill", (d) => d.color) // ✅ unique color
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
        .on("mouseout", () => setTooltip(null))
        .on("click", (_, d) => {
          if (onSelectTopic) onSelectTopic(d);
        });

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
    <div className="bg-black relative">
      <svg ref={svgRef}></svg>
      {tooltip && (
        <div
          className="absolute bg-black text-white text-sm px-2.5 py-1 border border-gray-300 rounded pointer-events-none"
          style={{ left: tooltip.x + 2, top: tooltip.y + 2 }}
        >
          {tooltip.content}
        </div>
      )}
    </div>
  );
};

export default BubbleChart;

