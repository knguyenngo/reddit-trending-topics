from datetime import datetime, timedelta
from airflow.sdk import DAG
from airflow.sdk.definitions.decorators import task
import sys
import os

# Add your project directory to Python path
PROJECT_DIR = os.path.expanduser('~/Projects/Reddit_Scraper/')
SCRIPTS_DIR = os.path.join(PROJECT_DIR, 'src/pipeline/')

default_args = {
    "depends_on_past": False,
    "retries": 0,  # Changed to 0 retries
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=2),  # Kill tasks that run too long
}

with DAG(
    "scrape_and_analyze",
    default_args=default_args,
    description="Scrape main page, gather comments, and analyze data",
    schedule=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["scraping", "analysis"],
) as dag:
    
    @task
    def scrape_main_page_task():
        """Scrape the main page and return the posts file path"""
        import io
        from contextlib import redirect_stdout
        
        # Add scripts directory to path
        if SCRIPTS_DIR not in sys.path:
            sys.path.insert(0, SCRIPTS_DIR)
        
        # Change to project directory
        os.chdir(PROJECT_DIR)
        
        print(f"Working directory: {os.getcwd()}")
        
        # Import the script module
        import scrape_main_page
        
        # Temporarily override sys.argv
        original_argv = sys.argv
        try:
            sys.argv = ['scrape_main_page.py', '-s', 'MMA', '-f', '72', '-u', '16', '-l', '1000', '-h']
            
            # Capture stdout to get the printed filename
            f = io.StringIO()
            with redirect_stdout(f):
                scrape_main_page.main()
            
            # Get all output and find the filename
            output = f.getvalue()
            print(f"Script output:\n{output}")
            
            # Extract the filename from output (last non-empty line typically)
            lines = [line.strip() for line in output.split('\n') if line.strip()]
            if not lines:
                raise ValueError("No output from scrape_main_page script")
            
            # The filename should be the last line or contains a path
            posts_file = lines[-1]
            
            print(f"Extracted posts file: {posts_file}")
            
            # Verify file exists
            if not os.path.exists(posts_file):
                raise FileNotFoundError(f"Posts file not found: {posts_file}")
            
            return posts_file
            
        finally:
            # Always restore original argv
            sys.argv = original_argv
    
    @task
    def gather_comments_task(posts_file: str):
        """Gather comments from scraped data"""
        print(f"Received posts file: {posts_file}")
        
        # Verify input file exists
        if not os.path.exists(posts_file):
            raise FileNotFoundError(f"Input file not found: {posts_file}")
        
        # Add scripts directory to path
        if SCRIPTS_DIR not in sys.path:
            sys.path.insert(0, SCRIPTS_DIR)
        
        # Change to project directory
        os.chdir(PROJECT_DIR)
        
        print(f"Working directory: {os.getcwd()}")
        
        # Import the script module
        import gather_comments
        
        # Temporarily override sys.argv
        original_argv = sys.argv
        try:
            sys.argv = ['gather_comments.py', '--input', posts_file]
            
            print(f"Running gather_comments with args: {sys.argv}")
            
            # Run the script
            gather_comments.main()
            
            print("Gather comments completed successfully")
            
        finally:
            # Always restore original argv
            sys.argv = original_argv
    
    @task
    def analyse_data_task():
        """Analyze the collected data"""
        # Add scripts directory to path
        if SCRIPTS_DIR not in sys.path:
            sys.path.insert(0, SCRIPTS_DIR)
        
        # CRITICAL: Change to the scripts directory where analyse_data.py expects to be run from
        # analyse_data.py uses relative paths: ../../data/raw
        # So we need to be in: ~/Projects/Reddit_Scraper/src/pipeline/
        scripts_dir = os.path.join(PROJECT_DIR, 'src/pipeline')
        os.chdir(scripts_dir)
        
        print(f"Working directory: {os.getcwd()}")
        
        # Build the expected paths
        raw_dir = os.path.abspath(os.path.join(os.getcwd(), '../../data/raw'))
        comment_dir = os.path.abspath(os.path.join(os.getcwd(), '../../data/raw/post_comments'))
        output_dir = os.path.abspath(os.path.join(os.getcwd(), '../../data/clean'))
        
        print(f"Expected raw directory: {raw_dir}")
        print(f"Expected comment directory: {comment_dir}")
        print(f"Expected output directory: {output_dir}")
        
        # Verify directories exist
        print(f"Raw directory exists: {os.path.exists(raw_dir)}")
        print(f"Comment directory exists: {os.path.exists(comment_dir)}")
        
        if os.path.exists(raw_dir):
            posts_files = [f for f in os.listdir(raw_dir) if f.startswith('posts_') and f.endswith('.json')]
            print(f"Found {len(posts_files)} posts files: {posts_files}")
        
        if os.path.exists(comment_dir):
            from pathlib import Path
            comment_files = list(Path(comment_dir).glob('*.json'))
            print(f"Found {len(comment_files)} comment files")
            if comment_files:
                print(f"Sample files: {[f.name for f in comment_files[:3]]}")
        else:
            print(f"WARNING: Comment directory does not exist: {comment_dir}")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Import and run the script module
        import analyse_data
        
        print("Running data analysis")
        analyse_data.main()
        
        print("Analysis completed successfully")
    
    # Define task dependencies with XCom (data passing)
    posts_file = scrape_main_page_task()
    gather_comments = gather_comments_task(posts_file)
    analyze = analyse_data_task()
    
    # Sequential execution
    gather_comments >> analyze
