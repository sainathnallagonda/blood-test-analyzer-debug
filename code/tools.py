## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

## Creating custom pdf reader tool
class BloodTestReportTool():
    async def read_data_tool(path='data/sample.pdf'):
        """Tool to read data from a pdf file from a path

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Blood Test report file
        """
        
        docs = PDFLoader(file_path=path).load()

        full_report = ""
        for data in docs:
            # Clean and format the report data
            content = data.page_content
            
            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
                
            full_report += content + "\n"
            
        return full_report

## Creating Nutrition Analysis Tool
class NutritionTool:
    async def analyze_nutrition_tool(blood_report_data):
        """Analyze blood report data to provide nutrition information

        Args:
            blood_report_data (str): The blood report data to analyze

        Returns:
            str: Results of the nutrition analysis
        """
        # Process and analyze the blood report data
        processed_data = blood_report_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement nutrition analysis logic here
        # Example: Return a fake but non-empty analysis for demonstration
        return "This is a sample nutrition analysis based on the provided blood report. All values are within normal range. Recommend a balanced diet and regular exercise."

## Creating Exercise Planning Tool
class ExerciseTool:
    async def create_exercise_plan_tool(blood_report_data):    
        """Create an exercise plan based on the blood report data

        Args:
            blood_report_data (str): The blood report data to base the exercise plan on

        Returns:
            str: The generated exercise plan
        """
        # TODO: Implement exercise planning logic here
        return "Exercise planning functionality to be implemented"