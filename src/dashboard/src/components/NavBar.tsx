// navbar/Navbar.tsx
"use client"
import React from 'react';

const Navbar: React.FC = () => {
  return (
    <nav className="flex justify-between items-center bg-black shadow-md px-6 py-3">
      {/* Logo / Left Side */}
      <div className="text-red-500 font-bold text-lg">
        Test
      </div>

      {/* Buttons / Right Side */}
      <div className="flex gap-4">
        <button className="px-4 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 transition">
          Home
        </button>
        <button className="px-4 py-2 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 transition">
          About
        </button>
        <button className="px-4 py-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600 transition">
          Contact
        </button>
      </div>
    </nav>
  );
};

export default Navbar;

