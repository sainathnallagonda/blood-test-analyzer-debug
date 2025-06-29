import csv
import os
from fpdf import FPDF

def save_analysis_to_csv(result_data, file_id, summary=None, pdf_path=None):
    """
    Save analysis results to a CSV file in output/csv/.
    result_data: list of dicts or a string (analysis text)
    file_id: unique identifier for the file/report
    summary: optional summary/analysis string to include in the CSV
    pdf_path: optional path to the generated PDF report
    """
    output_dir = os.path.join("output", "csv")
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"results_{file_id}.csv")
    if isinstance(result_data, list) and result_data:
        # Add summary/pdf_path to each row if provided
        if summary or pdf_path:
            for row in result_data:
                if summary:
                    row['analysis'] = summary
                if pdf_path:
                    row['pdf_report_path'] = pdf_path
            fieldnames = list(result_data[0].keys())
        else:
            fieldnames = result_data[0].keys()
        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(result_data)
        print(f"CSV generated: {csv_path}")
    elif isinstance(result_data, str) or summary:
        # Save the string/summary as a single-column CSV
        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            headers = ["analysis"]
            if pdf_path:
                headers.append("pdf_report_path")
            writer.writerow(headers)
            lines = summary.split('\n') if summary else result_data.split('\n')
            for line in lines:
                row = [line]
                if pdf_path:
                    row.append(pdf_path)
                writer.writerow(row)
        print(f"CSV (text) generated: {csv_path}")
    else:
        print("No valid data to write to CSV.")
    return csv_path

def save_analysis_to_pdf(result_text, file_id):
    """
    Save analysis results to a PDF file in output/reports/.
    result_text: string (the analysis result)
    file_id: unique identifier for the file/report
    """
    output_dir = os.path.join("output", "reports")
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f"report_{file_id}.pdf")
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        # Split long text into lines for PDF
        for line in result_text.split('\n'):
            pdf.multi_cell(0, 10, line)
        pdf.output(pdf_path)
        print(f"PDF generated: {pdf_path}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
    return pdf_path
