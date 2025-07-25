import { useEffect } from "react";

const NUM_LEAVES = 15;

const FallingLeaves = ({ imageSrc }) => {
  useEffect(() => {
    const container = document.getElementById("leaf-container");

    for (let i = 0; i < NUM_LEAVES; i++) {
      const leaf = document.createElement("img");
      leaf.src = imageSrc;
      leaf.className = "absolute w-8 h-8 animate-fall z-10 pointer-events-none";
      leaf.style.left = `${Math.random() * 100}vw`;
      leaf.style.animationDelay = `${Math.random() * 10}s`;
      container.appendChild(leaf);
    }
  }, [imageSrc]);

  return <div id="leaf-container" className="fixed top-0 left-0 w-full h-full overflow-hidden z-0"></div>;
};

export default FallingLeaves;