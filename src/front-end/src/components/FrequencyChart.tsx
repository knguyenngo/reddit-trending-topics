import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import type { UnigramFrequency } from "../types/index.ts"

function FrequencyChart(props: { data : UnigramFrequency}) {
  // Convert data into object for Recharts
  const chartData = Object.entries(props.data)
  .map(([word, count]) => ({
    name: word,
    value: count
  }))
  .sort((a, b) => b.value - a.value) // Sort by freq
  .slice(0, 15); // Top 15 words

  return (
    <div className="flex flex-col bg-red-500 rounded-[2rem] gap-4 w-full h-full p-4">
      <p className="self-center text-lg text-black">Top Unigrams</p>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData}>
          <XAxis 
            dataKey="name"
            stroke="888"
            fontSize={12}
            interval={0}
            angle={-45}
            textAnchor="end"
            height={65}
            dx={-5}
            dy={20}
          />
          <YAxis hide />
          <Tooltip />
          <Bar
            dataKey="value" 
            fill="#000000" 
            radius={[5, 5, 0, 0]} 
            barSize={40}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default FrequencyChart;
