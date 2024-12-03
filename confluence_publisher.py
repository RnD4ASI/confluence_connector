from atlassian import Confluence
from dotenv import load_dotenv
import os
import pandas as pd
from typing import List, Dict, Union

# Load environment variables
load_dotenv()

class ConfluencePublisher:
    def __init__(self):
        # Initialize Confluence client
        self.confluence = Confluence(
            url=os.getenv('CONFLUENCE_URL'),
            username=os.getenv('CONFLUENCE_USERNAME'),
            password=os.getenv('CONFLUENCE_API_TOKEN'),
            cloud=True
        )
        self.space_key = os.getenv('CONFLUENCE_SPACE')

    def create_latex_macro(self, latex: str) -> str:
        """Convert LaTeX to Confluence macro format"""
        # Using the {latex} macro which needs to be enabled in Confluence
        return f'<ac:structured-macro ac:name="latex">' \
               f'<ac:plain-text-body><![CDATA[{latex}]]></ac:plain-text-body>' \
               f'</ac:structured-macro>'

    def create_table_html(self, df: pd.DataFrame, with_latex: bool = False) -> str:
        """Convert pandas DataFrame to Confluence HTML table format"""
        html = '<table><tbody>'
        
        # Add header
        html += '<tr>'
        for col in df.columns:
            html += f'<th>{col}</th>'
        html += '</tr>'
        
        # Add rows
        for _, row in df.iterrows():
            html += '<tr>'
            for cell in row:
                if with_latex and str(cell).startswith('$') and str(cell).endswith('$'):
                    # Handle LaTeX in table cells
                    latex = str(cell)[1:-1]  # Remove $ symbols
                    cell_content = self.create_latex_macro(latex)
                else:
                    cell_content = str(cell)
                html += f'<td>{cell_content}</td>'
            html += '</tr>'
        
        html += '</tbody></table>'
        return html

    def publish_content(self, page_title: str, content: List[Dict[str, Union[str, pd.DataFrame]]]):
        """
        Publish content to Confluence page
        content: List of dictionaries with keys 'type' and 'data'
                type can be 'text', 'latex', or 'table'
        """
        html_content = []
        
        for item in content:
            if item['type'] == 'text':
                html_content.append(str(item['data']))
            elif item['type'] == 'latex':
                html_content.append(self.create_latex_macro(item['data']))
            elif item['type'] == 'table':
                html_content.append(
                    self.create_table_html(
                        item['data'],
                        with_latex=item.get('with_latex', False)
                    )
                )
        
        # Join all content
        final_content = '<br/>'.join(html_content)
        
        # Check if page exists
        page = self.confluence.get_page_by_title(
            space=self.space_key,
            title=page_title
        )
        
        if page:
            # Update existing page
            self.confluence.update_page(
                page_id=page['id'],
                title=page_title,
                body=final_content
            )
            print(f"Updated existing page: {page_title}")
        else:
            # Create new page
            self.confluence.create_page(
                space=self.space_key,
                title=page_title,
                body=final_content
            )
            print(f"Created new page: {page_title}")

# Example usage
if __name__ == "__main__":
    print("Confluence Publisher module loaded successfully")
