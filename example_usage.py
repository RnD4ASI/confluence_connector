from confluence_publisher import ConfluencePublisher
import pandas as pd

def create_sample_content():
    # Create a sample table with LaTeX formulas
    equations_df = pd.DataFrame({
        'Description': ['Einstein\'s Mass-Energy Equivalence', 'Newton\'s Second Law', 'Pythagorean Theorem'],
        'Formula': ['$E=mc^2$', '$F=ma$', '$a^2 + b^2 = c^2$']
    })

    # Create a sample data table
    data_df = pd.DataFrame({
        'Variable': ['x', 'y', 'z'],
        'Value': [10, 20, 30],
        'Unit': ['m/s', 'kg', 'N']
    })

    # Create content list with various types of content
    content = [
        {'type': 'text', 'data': '# Mathematical Equations and Data\n\nThis page demonstrates various mathematical equations and data tables.'},
        
        {'type': 'text', 'data': '\n## Important Equations\nBelow are some fundamental equations in physics:'},
        {'type': 'table', 'data': equations_df, 'with_latex': True},
        
        {'type': 'text', 'data': '\n## Complex Mathematical Expression\nHere\'s a more complex mathematical expression:'},
        {'type': 'latex', 'data': r'\int_{0}^{\infty} \frac{x^2}{e^x - 1} dx = \frac{\pi^4}{15}'},
        
        {'type': 'text', 'data': '\n## Experimental Data\nHere\'s a table of experimental measurements:'},
        {'type': 'table', 'data': data_df, 'with_latex': False},
        
        {'type': 'text', 'data': '\n## Matrix Expression\nAnd here\'s a matrix equation:'},
        {'type': 'latex', 'data': r'\begin{pmatrix} a & b \\ c & d \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} ax + by \\ cx + dy \end{pmatrix}'}
    ]
    
    return content

def main():
    try:
        # Initialize the publisher
        publisher = ConfluencePublisher()
        
        # Create the content
        content = create_sample_content()
        
        # Publish to Confluence
        page_title = "Mathematical Equations and Data"
        publisher.publish_content(page_title, content)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please make sure your .env file is properly configured with Confluence credentials.")

if __name__ == "__main__":
    main()
