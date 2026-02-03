// Parent - manages state
function SubredditSelector() {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>
        Toggle
      </button>
      
      {isOpen && <div>I'm the dropdown content!</div>}
    </div>
  );
}

export default SubredditSelector
