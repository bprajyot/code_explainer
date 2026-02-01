# ==========================================
# BACKEND - backend/app/storage/pdf_generator.py (CLIENT-READY)
# ==========================================
from ..models.schemas import CodeAnalysisResponse
from ..utils.logger import setup_logger
from datetime import datetime
import html

logger = setup_logger(__name__)

class PDFGenerator:
    def generate_formal_report(self, analysis: CodeAnalysisResponse, filename: str, code: str) -> str:
        """Generate client-ready professional PDF report"""
        logger.info("Generating client-ready PDF report")
        
        try:
            html_content = self._build_report_content(analysis, filename, code)
            return self._wrap_professional_template(html_content, filename)
        except Exception as e:
            logger.error(f"Error generating report: {e}", exc_info=True)
            return self._generate_fallback_report(analysis, filename, code)
    
    def _build_report_content(self, analysis: CodeAnalysisResponse, filename: str, code: str) -> str:
        """Build comprehensive report sections"""
        sections = []
        
        sections.append(self._generate_cover_page(filename, analysis))
        sections.append(self._generate_executive_summary(analysis))
        sections.append(self._generate_toc())
        sections.append(self._generate_overview_section(analysis))
        sections.append(self._generate_dependencies_section(analysis))
        sections.append(self._generate_functions_section(analysis))
        sections.append(self._generate_classes_section(analysis))
        sections.append(self._generate_quality_section(analysis))
        sections.append(self._generate_recommendations_section(analysis))
        sections.append(self._generate_appendix_section(code, analysis))
        
        return '\n'.join(sections)
    
    def _generate_cover_page(self, filename: str, analysis: CodeAnalysisResponse) -> str:
        """Professional cover page suitable for clients"""
        current_date = datetime.now()
        quality_score = "Excellent" if len(analysis.errors) == 0 else "Good" if len(analysis.errors) < 3 else "Satisfactory"
        
        return f"""
<div class="cover-page">
    <div class="cover-header">
        <div class="company-logo">
            <div class="logo-text">Code Analysis Report</div>
        </div>
    </div>
    
    <div class="cover-body">
        <h1 class="cover-title">{filename}</h1>
        <p class="cover-subtitle">Comprehensive Technical Analysis & Documentation</p>
        
        <div class="cover-divider"></div>
        
        <div class="cover-metrics">
            <div class="cover-metric">
                <div class="metric-number">{len(analysis.functions)}</div>
                <div class="metric-label">Functions Analyzed</div>
            </div>
            <div class="cover-metric">
                <div class="metric-number">{len(analysis.classes)}</div>
                <div class="metric-label">Classes Documented</div>
            </div>
            <div class="cover-metric">
                <div class="metric-number">{len(analysis.imports)}</div>
                <div class="metric-label">Dependencies Reviewed</div>
            </div>
        </div>
    </div>
    
    <div class="cover-footer">
        <table class="cover-info">
            <tr>
                <td class="info-label">Report Date:</td>
                <td class="info-value">{current_date.strftime("%B %d, %Y")}</td>
            </tr>
            <tr>
                <td class="info-label">Analysis System:</td>
                <td class="info-value">Python Code Explainer v2.0</td>
            </tr>
            <tr>
                <td class="info-label">Code Quality Rating:</td>
                <td class="info-value"><span class="quality-badge quality-{quality_score.lower()}">{quality_score}</span></td>
            </tr>
            <tr>
                <td class="info-label">Document Status:</td>
                <td class="info-value">Final - Ready for Review</td>
            </tr>
        </table>
        
        <div class="cover-confidential">
            <p>CONFIDENTIAL - FOR AUTHORIZED PERSONNEL ONLY</p>
        </div>
    </div>
</div>
<div class="page-break"></div>
"""
    
    def _generate_executive_summary(self, analysis: CodeAnalysisResponse) -> str:
        """Executive summary for stakeholders"""
        quality_assessment = "High" if len(analysis.errors) == 0 else "Medium" if len(analysis.errors) < 5 else "Requires Attention"
        
        return f"""
<div class="section">
    <h1 class="section-title">Executive Summary</h1>
    
    <div class="executive-box">
        <h3>Overview</h3>
        <p class="executive-text">{analysis.detailed_overview[:600]}...</p>
    </div>
    
    <h2 class="subsection-title">Key Findings</h2>
    
    <div class="findings-grid">
        <div class="finding-card finding-primary">
            <div class="finding-icon">✓</div>
            <div class="finding-content">
                <h4>Code Structure</h4>
                <p>Well-organized with {len(analysis.functions)} functions and {len(analysis.classes)} classes</p>
            </div>
        </div>
        
        <div class="finding-card finding-{'success' if len(analysis.errors) == 0 else 'warning'}">
            <div class="finding-icon">{'✓' if len(analysis.errors) == 0 else '⚠'}</div>
            <div class="finding-content">
                <h4>Quality Assessment</h4>
                <p>{quality_assessment} - {len(analysis.errors)} issue(s) identified</p>
            </div>
        </div>
        
        <div class="finding-card finding-info">
            <div class="finding-icon">📦</div>
            <div class="finding-content">
                <h4>Dependencies</h4>
                <p>{len(analysis.imports)} external libraries utilized</p>
            </div>
        </div>
        
        <div class="finding-card finding-primary">
            <div class="finding-icon">💡</div>
            <div class="finding-content">
                <h4>Recommendations</h4>
                <p>{len(analysis.suggestions)} improvement opportunities identified</p>
            </div>
        </div>
    </div>
    
    <h2 class="subsection-title">Code Metrics</h2>
    <table class="summary-table">
        <thead>
            <tr>
                <th>Metric</th>
                <th>Value</th>
                <th>Assessment</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Code Complexity</td>
                <td>{"Low" if len(analysis.functions) + len(analysis.classes) < 10 else "Medium"}</td>
                <td><span class="badge-success">✓ Manageable</span></td>
            </tr>
            <tr>
                <td>Code Quality Score</td>
                <td>{quality_assessment}</td>
                <td><span class="badge-{'success' if quality_assessment == 'High' else 'warning'}">{'✓ Excellent' if quality_assessment == 'High' else '⚠ Review Needed'}</span></td>
            </tr>
            <tr>
                <td>Documentation Coverage</td>
                <td>{sum(1 for f in analysis.functions if f.docstring) + sum(1 for c in analysis.classes if c.docstring)} / {len(analysis.functions) + len(analysis.classes)}</td>
                <td><span class="badge-info">ℹ Documented</span></td>
            </tr>
        </tbody>
    </table>
</div>
<div class="page-break"></div>
"""
    
    def _generate_toc(self) -> str:
        """Professional table of contents"""
        return """
<div class="section">
    <h1 class="section-title">Table of Contents</h1>
    
    <div class="toc-container">
        <div class="toc-section">
            <div class="toc-section-title">I. Overview & Analysis</div>
            <div class="toc-item">
                <span class="toc-number">1</span>
                <span class="toc-text">Executive Summary</span>
                <span class="toc-dots"></span>
                <span class="toc-page">2</span>
            </div>
            <div class="toc-item">
                <span class="toc-number">2</span>
                <span class="toc-text">Code Overview & Architecture</span>
                <span class="toc-dots"></span>
                <span class="toc-page">4</span>
            </div>
        </div>
        
        <div class="toc-section">
            <div class="toc-section-title">II. Technical Documentation</div>
            <div class="toc-item">
                <span class="toc-number">3</span>
                <span class="toc-text">External Dependencies</span>
                <span class="toc-dots"></span>
                <span class="toc-page">5</span>
            </div>
            <div class="toc-item">
                <span class="toc-number">4</span>
                <span class="toc-text">Functions Analysis</span>
                <span class="toc-dots"></span>
                <span class="toc-page">6</span>
            </div>
            <div class="toc-item">
                <span class="toc-number">5</span>
                <span class="toc-text">Classes & Methods</span>
                <span class="toc-dots"></span>
                <span class="toc-page">8</span>
            </div>
        </div>
        
        <div class="toc-section">
            <div class="toc-section-title">III. Quality & Recommendations</div>
            <div class="toc-item">
                <span class="toc-number">6</span>
                <span class="toc-text">Code Quality Assessment</span>
                <span class="toc-dots"></span>
                <span class="toc-page">10</span>
            </div>
            <div class="toc-item">
                <span class="toc-number">7</span>
                <span class="toc-text">Improvement Recommendations</span>
                <span class="toc-dots"></span>
                <span class="toc-page">11</span>
            </div>
        </div>
        
        <div class="toc-section">
            <div class="toc-section-title">IV. Appendices</div>
            <div class="toc-item">
                <span class="toc-number">A</span>
                <span class="toc-text">Complete Source Code</span>
                <span class="toc-dots"></span>
                <span class="toc-page">13</span>
            </div>
        </div>
    </div>
</div>
<div class="page-break"></div>
"""
    
    def _generate_overview_section(self, analysis: CodeAnalysisResponse) -> str:
        """Detailed overview section"""
        return f"""
<div class="section">
    <h1 class="section-title">1. Code Overview & Architecture</h1>
    
    <h2 class="subsection-title">1.1 Comprehensive Analysis</h2>
    <div class="content-block">
        {self._format_paragraphs(analysis.detailed_overview)}
    </div>
    
    <h2 class="subsection-title">1.2 Architectural Summary</h2>
    <div class="architecture-grid">
        <div class="arch-card">
            <div class="arch-icon">⚙️</div>
            <div class="arch-title">Programming Paradigm</div>
            <div class="arch-value">{"Object-Oriented" if analysis.classes else "Procedural"}</div>
        </div>
        <div class="arch-card">
            <div class="arch-icon">📊</div>
            <div class="arch-title">Complexity Level</div>
            <div class="arch-value">{"Low" if len(analysis.functions) + len(analysis.classes) < 10 else "Medium to High"}</div>
        </div>
        <div class="arch-card">
            <div class="arch-icon">🔧</div>
            <div class="arch-title">Modularity</div>
            <div class="arch-value">{"High" if len(analysis.functions) > 3 or len(analysis.classes) > 1 else "Standard"}</div>
        </div>
    </div>
</div>
<div class="page-break"></div>
"""
    
    def _generate_dependencies_section(self, analysis: CodeAnalysisResponse) -> str:
        """Dependencies section"""
        content = f"""
<div class="section">
    <h1 class="section-title">2. External Dependencies</h1>
    
    <div class="intro-text">
        <p>This codebase utilizes <strong>{len(analysis.imports)}</strong> external dependencies. Each dependency has been analyzed for its purpose, usage, and integration within the system.</p>
    </div>
    
"""
        
        if analysis.imports:
            for idx, imp in enumerate(analysis.imports, 1):
                content += f"""
    <div class="dependency-card">
        <div class="dependency-header">
            <span class="dep-number">{idx}</span>
            <h3 class="dep-title">{imp.module}</h3>
        </div>
        <div class="dependency-body">
            <div class="dep-row">
                <span class="dep-label">Imported Components:</span>
                <span class="dep-value">{', '.join(f'<code>{n}</code>' for n in imp.names)}</span>
            </div>
            <div class="dep-row">
                <span class="dep-label">Source Line:</span>
                <span class="dep-value">Line {imp.line_number}</span>
            </div>
            <div class="dep-purpose">
                <span class="dep-label">Purpose & Integration:</span>
                <p>{imp.purpose}</p>
            </div>
        </div>
    </div>
"""
        else:
            content += '<div class="info-message">No external dependencies detected. This code uses only Python standard library components.</div>'
        
        content += """
</div>
<div class="page-break"></div>
"""
        return content
    
    def _generate_functions_section(self, analysis: CodeAnalysisResponse) -> str:
        """Functions section"""
        content = """
<div class="section">
    <h1 class="section-title">3. Functions Analysis</h1>
    
"""
        if analysis.functions:
            for idx, func in enumerate(analysis.functions, 1):
                params_str = ', '.join(func.parameters) if func.parameters else 'None'
                content += f"""
    <div class="component-card">
        <div class="component-header">
            <h2 class="component-title">
                <span class="component-number">{idx}.</span>
                <code class="component-name">{func.name}({params_str})</code>
            </h2>
        </div>
        
        <div class="component-meta">
            <div class="meta-item">
                <span class="meta-label">Returns:</span>
                <code>{func.return_type or 'Not specified'}</code>
            </div>
            <div class="meta-item">
                <span class="meta-label">Defined:</span>
                Line {func.line_number}
            </div>
            <div class="meta-item">
                <span class="meta-label">Usage:</span>
                {len(set(func.occurrences)) if func.occurrences else 0} call(s)
            </div>
        </div>
        
        {"<div class='documentation-box'><div class='doc-label'>Documentation:</div><pre>" + html.escape(func.docstring) + "</pre></div>" if func.docstring else ""}
        
        <div class="explanation-box">
            <div class="explanation-label">Technical Analysis:</div>
            <div class="explanation-content">
                {func.logic_explanation or '<p class="no-content">Detailed analysis not available</p>'}
            </div>
        </div>
        
        {"<div class='variables-used'><strong>Variables Used:</strong> " + ', '.join(f'<code>{v}</code>' for v in func.variables_used) + "</div>" if func.variables_used else ""}
    </div>
"""
        else:
            content += '<div class="info-message">No standalone functions defined in this module.</div>'
        
        content += """
</div>
<div class="page-break"></div>
"""
        return content
    
    def _generate_classes_section(self, analysis: CodeAnalysisResponse) -> str:
        """Classes section"""
        content = """
<div class="section">
    <h1 class="section-title">4. Classes & Methods Documentation</h1>
    
"""
        if analysis.classes:
            for idx, cls in enumerate(analysis.classes, 1):
                content += f"""
    <div class="component-card">
        <div class="component-header">
            <h2 class="component-title">
                <span class="component-number">{idx}.</span>
                <code class="component-name">{cls.name}</code>
            </h2>
        </div>
        
        <div class="component-meta">
            <div class="meta-item">
                <span class="meta-label">Inheritance:</span>
                {', '.join(cls.base_classes) if cls.base_classes else 'None'}
            </div>
            <div class="meta-item">
                <span class="meta-label">Methods:</span>
                {len(cls.methods)}
            </div>
            <div class="meta-item">
                <span class="meta-label">Attributes:</span>
                {len(cls.attributes)}
            </div>
            <div class="meta-item">
                <span class="meta-label">Defined:</span>
                Line {cls.line_number}
            </div>
        </div>
        
        {"<div class='documentation-box'><div class='doc-label'>Class Documentation:</div><pre>" + html.escape(cls.docstring) + "</pre></div>" if cls.docstring else ""}
        
        <div class="explanation-box">
            <div class="explanation-label">Class Overview:</div>
            <div class="explanation-content">
                {cls.detailed_explanation or '<p class="no-content">Overview not available</p>'}
            </div>
        </div>
        
        <div class="subsection">
            <h3 class="subsection-heading">Attributes</h3>
            <div class="attributes-list">
                {', '.join(f'<code>{attr}</code>' for attr in cls.attributes) if cls.attributes else '<em>No attributes defined</em>'}
            </div>
        </div>
        
        <div class="subsection">
            <h3 class="subsection-heading">Methods</h3>
"""
                
                if cls.methods:
                    if isinstance(cls.method_explanations, dict) and cls.method_explanations:
                        for method_idx, method in enumerate(cls.methods, 1):
                            explanation = cls.method_explanations.get(method, "Method analysis not available")
                            content += f"""
            <div class="method-card">
                <div class="method-header">
                    <span class="method-number">{method_idx}.</span>
                    <code class="method-name">{method}()</code>
                </div>
                <div class="method-content">
                    {explanation}
                </div>
            </div>
"""
                    else:
                        for method_idx, method in enumerate(cls.methods, 1):
                            content += f"""
            <div class="method-card">
                <div class="method-header">
                    <span class="method-number">{method_idx}.</span>
                    <code class="method-name">{method}()</code>
                </div>
                <div class="method-content">
                    <em>Detailed analysis not available</em>
                </div>
            </div>
"""
                else:
                    content += '<div class="no-content">No methods defined</div>'
                
                content += """
        </div>
    </div>
"""
        else:
            content += '<div class="info-message">No classes defined in this module.</div>'
        
        content += """
</div>
<div class="page-break"></div>
"""
        return content
    
    def _generate_quality_section(self, analysis: CodeAnalysisResponse) -> str:
        """Quality assessment"""
        quality_score = "Excellent" if len(analysis.errors) == 0 else "Good" if len(analysis.errors) < 5 else "Needs Improvement"
        
        content = f"""
<div class="section">
    <h1 class="section-title">5. Code Quality Assessment</h1>
    
    <div class="quality-overview">
        <div class="quality-score-card">
            <div class="score-icon">{'✓' if len(analysis.errors) == 0 else '⚠'}</div>
            <div class="score-label">Overall Quality Rating</div>
            <div class="score-value score-{quality_score.lower().replace(' ', '-')}">{quality_score}</div>
            <div class="score-detail">{len(analysis.errors)} Issue(s) Detected</div>
        </div>
    </div>
    
"""
        
        if analysis.errors:
            critical = [e for e in analysis.errors if e.severity == 'Critical']
            warnings = [e for e in analysis.errors if e.severity == 'Warning']
            
            if critical:
                content += """
    <h2 class="subsection-title">Critical Issues</h2>
"""
                for idx, error in enumerate(critical, 1):
                    content += f"""
    <div class="issue-card issue-critical">
        <div class="issue-header">
            <span class="issue-icon">🔴</span>
            <span class="issue-number">Issue {idx}</span>
            <span class="issue-category">{error.category}</span>
        </div>
        <div class="issue-body">
            <p>{error.message}</p>
            {"<div class='issue-location'>Location: Line " + str(error.line_number) + "</div>" if error.line_number else ""}
        </div>
    </div>
"""
            
            if warnings:
                content += """
    <h2 class="subsection-title">Warnings</h2>
"""
                for idx, error in enumerate(warnings, 1):
                    content += f"""
    <div class="issue-card issue-warning">
        <div class="issue-header">
            <span class="issue-icon">🟡</span>
            <span class="issue-number">Warning {idx}</span>
            <span class="issue-category">{error.category}</span>
        </div>
        <div class="issue-body">
            <p>{error.message}</p>
            {"<div class='issue-location'>Location: Line " + str(error.line_number) + "</div>" if error.line_number else ""}
        </div>
    </div>
"""
        else:
            content += """
    <div class="success-message">
        <div class="success-icon">✓</div>
        <div class="success-text">
            <h3>Excellent Code Quality</h3>
            <p>No critical issues or warnings detected. The codebase demonstrates strong adherence to best practices and quality standards.</p>
        </div>
    </div>
"""
        
        content += """
</div>
<div class="page-break"></div>
"""
        return content
    
    def _generate_recommendations_section(self, analysis: CodeAnalysisResponse) -> str:
        """Recommendations"""
        content = """
<div class="section">
    <h1 class="section-title">6. Improvement Recommendations</h1>
    
    <div class="intro-text">
        <p>The following recommendations are provided to enhance code quality, maintainability, and performance. Each recommendation is prioritized based on impact and implementation effort.</p>
    </div>
    
"""
        
        if analysis.suggestions:
            high = [s for s in analysis.suggestions if s.priority == 'High']
            medium = [s for s in analysis.suggestions if s.priority == 'Medium']
            low = [s for s in analysis.suggestions if s.priority == 'Low']
            
            if high:
                content += """
    <h2 class="subsection-title">High Priority Recommendations</h2>
"""
                for idx, s in enumerate(high, 1):
                    content += f"""
    <div class="recommendation-card priority-high">
        <div class="rec-header">
            <span class="rec-number">{idx}</span>
            <h3 class="rec-title">{s.title}</h3>
            <span class="rec-category">{s.category}</span>
        </div>
        <div class="rec-body">
            <p>{s.description}</p>
            {"<div class='code-sample'><div class='sample-label'>Implementation Example:</div><pre><code>" + html.escape(s.code_example) + "</code></pre></div>" if s.code_example else ""}
        </div>
    </div>
"""
            
            if medium:
                content += """
    <h2 class="subsection-title">Medium Priority Recommendations</h2>
"""
                for idx, s in enumerate(medium, 1):
                    content += f"""
    <div class="recommendation-card priority-medium">
        <div class="rec-header">
            <span class="rec-number">{idx}</span>
            <h3 class="rec-title">{s.title}</h3>
            <span class="rec-category">{s.category}</span>
        </div>
        <div class="rec-body">
            <p>{s.description}</p>
        </div>
    </div>
"""
            
            if low:
                content += """
    <h2 class="subsection-title">Low Priority Recommendations</h2>
    <ul class="low-priority-list">
"""
                for s in low:
                    content += f'<li><strong>{s.title}</strong> ({s.category}): {s.description}</li>'
                content += """
    </ul>
"""
        else:
            content += '<div class="info-message">No specific recommendations at this time. The codebase demonstrates good quality standards.</div>'
        
        content += """
</div>
<div class="page-break"></div>
"""
        return content
    
    def _generate_appendix_section(self, code: str, analysis: CodeAnalysisResponse) -> str:
        """Appendix"""
        return f"""
<div class="section">
    <h1 class="section-title">Appendix A: Complete Source Code</h1>
    
    <div class="source-code-container">
        <pre class="source-code"><code class="language-python">{html.escape(code)}</code></pre>
    </div>
    
    <h1 class="section-title" style="margin-top: 60px;">Appendix B: Analysis Metadata</h1>
    
    <table class="metadata-table">
        <tr>
            <td class="meta-key">Total Lines of Code:</td>
            <td class="meta-value">{len(code.split(chr(10)))}</td>
        </tr>
        <tr>
            <td class="meta-key">Total Characters:</td>
            <td class="meta-value">{len(code):,}</td>
        </tr>
        <tr>
            <td class="meta-key">Analysis Timestamp:</td>
            <td class="meta-value">{datetime.now().strftime("%B %d, %Y at %I:%M:%S %p")}</td>
        </tr>
        <tr>
            <td class="meta-key">Analysis System Version:</td>
            <td class="meta-value">Python Code Explainer v2.0</td>
        </tr>
        <tr>
            <td class="meta-key">Report Format:</td>
            <td class="meta-value">Professional Technical Documentation</td>
        </tr>
    </table>
</div>
"""
    
    def _format_paragraphs(self, text: str) -> str:
        """Format text into paragraphs"""
        paragraphs = text.split('\n\n')
        return ''.join(f'<p class="content-paragraph">{p.strip()}</p>' for p in paragraphs if p.strip())
    
    def _generate_fallback_report(self, analysis: CodeAnalysisResponse, filename: str, code: str) -> str:
        """Simple fallback if main generation fails"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Analysis Report - {filename}</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 40px; max-width: 1200px; margin: 0 auto; line-height: 1.8; }}
        h1 {{ color: #1e3c72; border-bottom: 3px solid #1e3c72; padding-bottom: 10px; }}
        .section {{ margin: 40px 0; padding: 30px; background: #f8f9fa; border-radius: 10px; }}
        code {{ background: #e9ecef; padding: 3px 8px; border-radius: 4px; }}
        pre {{ background: #2d3748; color: #e2e8f0; padding: 20px; border-radius: 8px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>Code Analysis Report: {filename}</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime("%B %d, %Y")}</p>
    <div class="section">
        <h2>Overview</h2>
        <p>{analysis.detailed_overview}</p>
    </div>
    <div class="section">
        <h2>Statistics</h2>
        <p>Functions: {len(analysis.functions)} | Classes: {len(analysis.classes)} | Issues: {len(analysis.errors)}</p>
    </div>
</body>
</html>
"""
    
    def _wrap_professional_template(self, content: str, filename: str) -> str:
        """Professional HTML template with client-ready styling"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technical Analysis Report - {filename}</title>
    <style>
        /* Professional Client-Ready Styling */
        @page {{
            size: A4;
            margin: 2cm;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Calibri', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.7;
            color: #2c3e50;
            background: #ffffff;
        }}
        
        /* Cover Page */
        .cover-page {{
            height: 100vh;
            display: flex;
            flex-direction: column;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7a9cc6 100%);
            color: white;
            padding: 60px;
            position: relative;
        }}
        
        .company-logo {{
            text-align: center;
            margin-bottom: 80px;
        }}
        
        .logo-icon {{
            font-size: 80px;
            margin-bottom: 20px;
        }}
        
        .logo-text {{
            font-size: 28pt;
            font-weight: 300;
            letter-spacing: 4px;
            text-transform: uppercase;
        }}
        
        .cover-body {{
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
        }}
        
        .cover-title {{
            font-size: 42pt;
            font-weight: 600;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .cover-subtitle {{
            font-size: 18pt;
            font-weight: 300;
            opacity: 0.95;
            margin-bottom: 60px;
        }}
        
        .cover-divider {{
            width: 200px;
            height: 3px;
            background: white;
            margin: 40px auto;
            opacity: 0.7;
        }}
        
        .cover-metrics {{
            display: flex;
            justify-content: center;
            gap: 60px;
            margin: 40px 0;
        }}
        
        .cover-metric {{
            text-align: center;
        }}
        
        .metric-number {{
            font-size: 48pt;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .metric-label {{
            font-size: 12pt;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .cover-footer {{
            margin-top: auto;
        }}
        
        .cover-info {{
            width: 100%;
            max-width: 700px;
            margin: 0 auto 40px;
            border-collapse: collapse;
        }}
        
        .cover-info tr {{
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }}
        
        .info-label {{
            padding: 15px 20px;
            font-weight: 600;
            text-align: left;
            width: 50%;
        }}
        
        .info-value {{
            padding: 15px 20px;
            text-align: right;
        }}
        
        .quality-badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 10pt;
        }}
        
        .quality-excellent {{
            background: #28a745;
            color: white;
        }}
        
        .quality-good {{
            background: #ffc107;
            color: #000;
        }}
        
        .quality-satisfactory {{
            background: #ff9800;
            color: white;
        }}
        
        .cover-confidential {{
            text-align: center;
            font-size: 9pt;
            opacity: 0.8;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.3);
        }}
        
        /* Sections */
        .section {{
            padding: 50px 60px;
        }}
        
        .section-title {{
            font-size: 28pt;
            font-weight: 700;
            color: #1e3c72;
            margin-bottom: 40px;
            padding-bottom: 15px;
            border-bottom: 4px solid #1e3c72;
        }}
        
        .subsection-title {{
            font-size: 18pt;
            font-weight: 600;
            color: #2a5298;
            margin: 40px 0 20px 0;
        }}
        
        .subsection-heading {{
            font-size: 14pt;
            font-weight: 600;
            color: #34495e;
            margin: 25px 0 15px 0;
            padding-left: 15px;
            border-left: 4px solid #3498db;
        }}
        
        /* Executive Summary */
        .executive-box {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-left: 6px solid #1e3c72;
            padding: 30px;
            margin: 30px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .executive-box h3 {{
            color: #1e3c72;
            font-size: 16pt;
            margin-bottom: 20px;
        }}
        
        .executive-text {{
            font-size: 11.5pt;
            line-height: 1.9;
            text-align: justify;
        }}
        
        .findings-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
            margin: 30px 0;
        }}
        
        .finding-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 25px;
            display: flex;
            gap: 20px;
            transition: transform 0.2s;
        }}
        
        .finding-primary {{
            border-left: 5px solid #1e3c72;
        }}
        
        .finding-success {{
            border-left: 5px solid #28a745;
        }}
        
        .finding-warning {{
            border-left: 5px solid #ffc107;
        }}
        
        .finding-info {{
            border-left: 5px solid #17a2b8;
        }}
        
        .finding-icon {{
            font-size: 32pt;
            flex-shrink: 0;
        }}
        
        .finding-content h4 {{
            color: #2c3e50;
            font-size: 13pt;
            margin-bottom: 10px;
        }}
        
        .finding-content p {{
            color: #6c757d;
            font-size: 10pt;
            line-height: 1.6;
        }}
        
        /* Tables */
        .summary-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .summary-table thead {{
            background: #1e3c72;
            color: white;
        }}
        
        .summary-table th {{
            padding: 18px 20px;
            text-align: left;
            font-weight: 600;
            font-size: 11pt;
        }}
        
        .summary-table td {{
            padding: 16px 20px;
            border-bottom: 1px solid #e9ecef;
            font-size: 10.5pt;
        }}
        
        .summary-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .summary-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .badge-success {{
            background: #d4edda;
            color: #155724;
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 9pt;
            font-weight: 600;
        }}
        
        .badge-warning {{
            background: #fff3cd;
            color: #856404;
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 9pt;
            font-weight: 600;
        }}
        
        .badge-info {{
            background: #d1ecf1;
            color: #0c5460;
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 9pt;
            font-weight: 600;
        }}
        
        /* Table of Contents */
        .toc-container {{
            padding: 20px;
        }}
        
        .toc-section {{
            margin: 30px 0;
        }}
        
        .toc-section-title {{
            font-size: 13pt;
            font-weight: 700;
            color: #1e3c72;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .toc-item {{
            display: flex;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px dotted #cbd5e0;
        }}
        
        .toc-number {{
            font-weight: 700;
            color: #1e3c72;
            width: 50px;
            flex-shrink: 0;
        }}
        
        .toc-text {{
            flex-grow: 1;
            font-size: 11pt;
        }}
        
        .toc-dots {{
            flex-grow: 1;
            border-bottom: 2px dotted #cbd5e0;
            margin: 0 15px;
        }}
        
        .toc-page {{
            width: 50px;
            text-align: right;
            color: #6c757d;
            font-weight: 600;
        }}
        
        /* Content Blocks */
        .content-block {{
            background: #f8f9fa;
            padding: 30px;
            margin: 25px 0;
            border-radius: 8px;
            border-left: 5px solid #2a5298;
        }}
        
        .content-paragraph {{
            margin: 15px 0;
            text-align: justify;
            line-height: 1.8;
        }}
        
        .architecture-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 25px;
            margin: 30px 0;
        }}
        
        .arch-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
        }}
        
        .arch-icon {{
            font-size: 40pt;
            margin-bottom: 15px;
        }}
        
        .arch-title {{
            font-size: 10pt;
            color: #6c757d;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .arch-value {{
            font-size: 16pt;
            font-weight: 700;
            color: #1e3c72;
        }}
        
        /* Dependencies */
        .dependency-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            margin: 25px 0;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}
        
        .dependency-header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px 30px;
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .dep-number {{
            background: white;
            color: #1e3c72;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14pt;
        }}
        
        .dep-title {{
            font-size: 16pt;
            font-weight: 600;
            margin: 0;
        }}
        
        .dependency-body {{
            padding: 25px 30px;
        }}
        
        .dep-row {{
            display: flex;
            padding: 12px 0;
            border-bottom: 1px solid #f1f3f5;
        }}
        
        .dep-label {{
            font-weight: 600;
            color: #495057;
            min-width: 180px;
        }}
        
        .dep-value code {{
            background: #e9ecef;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Consolas', monospace;
            font-size: 9.5pt;
            color: #c7254e;
        }}
        
        .dep-purpose {{
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        
        .dep-purpose p {{
            margin-top: 10px;
            line-height: 1.8;
            text-align: justify;
        }}
        
        /* Component Cards (Functions/Classes) */
        .component-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            margin: 30px 0;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        
        .component-header {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px 30px;
            border-bottom: 3px solid #1e3c72;
        }}
        
        .component-title {{
            display: flex;
            align-items: center;
            gap: 15px;
            color: #1e3c72;
            font-size: 18pt;
            margin: 0;
        }}
        
        .component-number {{
            background: #1e3c72;
            color: white;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
        }}
        
        .component-name {{
            font-family: 'Consolas', monospace;
            background: #2d3748;
            color: #e2e8f0;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 13pt;
        }}
        
        .component-meta {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 25px 30px;
            background: #fafbfc;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .meta-item {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        
        .meta-label {{
            font-size: 9pt;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}
        
        .meta-item code {{
            background: #e9ecef;
            padding: 4px 10px;
            border-radius: 4px;
            font-family: 'Consolas', monospace;
            font-size: 10pt;
            color: #c7254e;
        }}
        
        .documentation-box {{
            margin: 25px 30px;
            padding: 20px;
            background: #fffbf0;
            border: 1px solid #ffd966;
            border-radius: 6px;
        }}
        
        .doc-label {{
            font-weight: 600;
            color: #856404;
            margin-bottom: 10px;
            font-size: 10pt;
        }}
        
        .documentation-box pre {{
            background: transparent;
            border: none;
            padding: 10px 0;
            margin: 0;
            color: #495057;
            font-size: 10pt;
            white-space: pre-wrap;
        }}
        
        .explanation-box {{
            margin: 25px 30px;
            padding: 25px;
            background: #f0f7ff;
            border-left: 5px solid #2a5298;
            border-radius: 6px;
        }}
        
        .explanation-label {{
            font-weight: 700;
            color: #1e3c72;
            margin-bottom: 15px;
            font-size: 11pt;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .explanation-content {{
            line-height: 1.9;
            text-align: justify;
        }}
        
        .variables-used {{
            margin: 25px 30px;
            padding: 15px 20px;
            background: #f8f9fa;
            border-radius: 6px;
            font-size: 10pt;
        }}
        
        .variables-used code {{
            background: #e9ecef;
            padding: 3px 8px;
            border-radius: 4px;
            margin: 0 5px;
        }}
        
        .subsection {{
            margin: 30px 30px;
        }}
        
        .attributes-list {{
            padding: 15px 20px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        
        .attributes-list code {{
            background: #e9ecef;
            padding: 4px 10px;
            border-radius: 4px;
            margin: 0 8px 8px 0;
            display: inline-block;
        }}
        
        /* Methods */
        .method-card {{
            background: #fafbfc;
            border: 1px solid #e1e4e8;
            border-left: 4px solid #6c757d;
            padding: 20px;
            margin: 15px 0;
            border-radius: 6px;
        }}
        
        .method-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}
        
        .method-number {{
            background: #6c757d;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 10pt;
        }}
        
        .method-name {{
            font-family: 'Consolas', monospace;
            background: #2d3748;
            color: #e2e8f0;
            padding: 6px 14px;
            border-radius: 4px;
            font-size: 11pt;
        }}
        
        .method-content {{
            line-height: 1.8;
            color: #495057;
            padding-left: 42px;
        }}
        
        /* Quality Section */
        .quality-overview {{
            margin: 40px 0;
            display: flex;
            justify-content: center;
        }}
        
        .quality-score-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 3px solid #1e3c72;
            border-radius: 15px;
            padding: 50px;
            text-align: center;
            min-width: 400px;
        }}
        
        .score-icon {{
            font-size: 72pt;
            margin-bottom: 20px;
        }}
        
        .score-label {{
            font-size: 11pt;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 15px;
        }}
        
        .score-value {{
            font-size: 36pt;
            font-weight: 700;
            margin-bottom: 15px;
        }}
        
        .score-excellent {{
            color: #28a745;
        }}
        
        .score-good {{
            color: #ffc107;
        }}
        
        .score-needs-improvement {{
            color: #dc3545;
        }}
        
        .score-detail {{
            font-size: 12pt;
            color: #495057;
        }}
        
        /* Issues */
        .issue-card {{
            border-radius: 8px;
            padding: 25px;
            margin: 20px 0;
            border-left-width: 6px;
            border-left-style: solid;
        }}
        
        .issue-critical {{
            background: #fff5f5;
            border-color: #dc3545;
        }}
        
        .issue-warning {{
            background: #fffbf0;
            border-color: #ffc107;
        }}
        
        .issue-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        .issue-icon {{
            font-size: 24pt;
        }}
        
        .issue-number {{
            font-weight: 700;
            font-size: 11pt;
        }}
        
        .issue-category {{
            background: rgba(0,0,0,0.1);
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 9pt;
            font-weight: 600;
        }}
        
        .issue-body {{
            padding-left: 55px;
        }}
        
        .issue-location {{
            margin-top: 10px;
            font-size: 9pt;
            color: #6c757d;
            font-style: italic;
        }}
        
        /* Success */
        .success-message {{
            background: #d4edda;
            border: 2px solid #c3e6cb;
            border-radius: 10px;
            padding: 40px;
            display: flex;
            align-items: center;
            gap: 30px;
        }}
        
        .success-icon {{
            font-size: 64pt;
            color: #28a745;
        }}
        
        .success-text h3 {{
            color: #155724;
            font-size: 18pt;
            margin-bottom: 10px;
        }}
        
        .success-text p {{
            color: #155724;
            line-height: 1.8;
        }}
        
        /* Recommendations */
        .recommendation-card {{
            border-radius: 10px;
            padding: 30px;
            margin: 25px 0;
            border-left-width: 6px;
            border-left-style: solid;
        }}
        
        .priority-high {{
            background: #fff5f5;
            border-color: #dc3545;
        }}
        
        .priority-medium {{
            background: #fffbf0;
            border-color: #ffc107;
        }}
        
        .rec-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .rec-number {{
            background: #1e3c72;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14pt;
        }}
        
        .rec-title {{
            flex-grow: 1;
            color: #2c3e50;
            font-size: 14pt;
            margin: 0;
        }}
        
        .rec-category {{
            background: rgba(0,0,0,0.08);
            padding: 6px 14px;
            border-radius: 14px;
            font-size: 9pt;
            font-weight: 600;
        }}
        
        .rec-body {{
            line-height: 1.9;
            padding-left: 55px;
        }}
        
        .code-sample {{
            margin-top: 20px;
            background: #2d3748;
            border-radius: 8px;
            padding: 20px;
        }}
        
        .sample-label {{
            color: #e2e8f0;
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 10pt;
        }}
        
        .code-sample pre {{
            background: transparent;
            border: none;
            padding: 0;
            margin: 0;
        }}
        
        .code-sample code {{
            color: #e2e8f0;
            background: transparent;
            font-size: 9.5pt;
        }}
        
        .low-priority-list {{
            list-style: none;
            padding: 0;
        }}
        
        .low-priority-list li {{
            background: #f8f9fa;
            padding: 20px;
            margin: 12px 0;
            border-left: 4px solid #6c757d;
            border-radius: 6px;
            line-height: 1.8;
        }}
        
        /* Source Code */
        .source-code-container {{
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 5px;
            margin: 30px 0;
        }}
        
        .source-code {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 30px;
            border-radius: 8px;
            overflow-x: auto;
            max-height: 800px;
            font-size: 9pt;
            line-height: 1.6;
        }}
        
        .source-code code {{
            color: #e2e8f0;
            background: transparent;
        }}
        
        /* Metadata */
        .metadata-table {{
            width: 100%;
            max-width: 700px;
            border-collapse: collapse;
            margin: 30px 0;
        }}
        
        .metadata-table tr {{
            border-bottom: 1px solid #e9ecef;
        }}
        
        .meta-key {{
            padding: 15px 20px;
            font-weight: 600;
            color: #495057;
            width: 60%;
        }}
        
        .meta-value {{
            padding: 15px 20px;
            color: #6c757d;
        }}
        
        /* Messages */
        .info-message {{
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 8px;
            padding: 20px;
            color: #0c5460;
            text-align: center;
            font-style: italic;
        }}
        
        .intro-text {{
            background: #f8f9fa;
            padding: 20px 30px;
            border-left: 5px solid #2a5298;
            margin: 25px 0;
            border-radius: 6px;
        }}
        
        .intro-text p {{
            line-height: 1.8;
            text-align: justify;
        }}
        
        .no-content {{
            color: #999;
            font-style: italic;
            padding: 20px;
            text-align: center;
        }}
        
        /* Page Breaks */
        .page-break {{
            page-break-after: always;
        }}
        
        /* Print Optimization */
        @media print {{
            .page-break {{
                page-break-after: always;
            }}
            
            body {{
                font-size: 10pt;
            }}
            
            .section {{
                padding: 30px 40px;
            }}
        }}
    </style>
</head>
<body>
    {content}
</body>
</html>"""