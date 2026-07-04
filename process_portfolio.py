#!/usr/bin/env python3

import os
import json
from pathlib import Path

def discover_projects(root_path):
    """Discover and categorize projects in the cx3 folder."""
    projects = []
    for item in root_path.iterdir():
        if item.is_dir():
            # Check if it's a project directory
            project_file = item / "project.json"
            if project_file.exists():
                with open(project_file) as f:
                    project = json.load(f)
                    project["path"] = str(item)
                    project["type"] = "full_project"
                    projects.append(project)
    return projects

def generate_readme_for_platform(projects, platform):
    """Generate README content for a specific platform."""
    if platform == "web":
        return generate_web_readme(projects)
    elif platform == "github":
        return generate_github_readme(projects)
    elif platform == "summary":
        return generate_summary_readme(projects)
    else:
        return ""

def generate_web_readme(projects):
    """Generate README for web/platform overview."""
    content = "# Engineering Portfolio Overview\n\n"
    content += "This portfolio showcases engineering projects including CAD designs, Python applications, and automated systems.\n\n"
    
    content += "## Active Projects\n\n"
    for project in projects:
        content += f"### {project['name']}\n\n"
        content += f"{project.get('description', 'Engineering project')}\n\n"
        if project.get('technologies'):
            content += f"**Technologies:** {', '.join(project['technologies'])}\n\n"
        if project.get('links'):
            links = []
            for platform, url in project['links'].items():
                if platform == 'github' and 'github.com' in url:
                    links.append(f"[GitHub]({url})")
                elif platform == 'demo' and 'github.io' in url:
                    links.append(f"[Live Demo]({url})")
            if links:
                content += f"**Links:** {', '.join(links)}\n\n"
        content += "---\n\n"
    
    return content

def generate_github_readme(projects):
    """Generate README for GitHub README.md."""
    content = "# cx3 Engineering Portfolio\n\n"
    content += "Collection of engineering projects including CAD designs, Python applications, and automated systems for aerospace and mechanical engineering.\n\n"
    
    content += "## Projects\n\n"
    
    for project in projects:
        content += f"### {project['name']}\n\n"
        content += f"{project.get('description', 'Engineering project')}\n\n"
        
        if project.get('technologies'):
            tech_list = ' '.join([f"`{t}`" for t in project['technologies']])
            content += f"**Technologies:** {tech_list}\n\n"
        
        content += "| **Link** | **Type** |\n"
        content += "|----------|----------|\n"
        
        if project.get('links'):
            for platform, url in project['links'].items():
                if 'github.io' in url:
                    content += f"|[{platform.title()} Demo]({url})|Live|\n"
                elif 'github.com' in url:
                    content += f"|[{platform.title()} Code]({url})|Repository|\n"
        
        content += "\n"
    
    content += f"**Total Projects:** {len(projects)}\n\n"
    return content

def generate_summary_readme(projects):
    """Generate concise summary README."""
    content = "# cx3 Engineering Projects Summary\n\n"
    content += f"Total projects: {len(projects)}\n"
    
    tech_summary = {}
    for project in projects:
        for tech in project.get('technologies', []):
            tech_summary[tech] = tech_summary.get(tech, 0) + 1
    
    content += "\n**Technologies Used:**\n"
    for tech, count in sorted(tech_summary.items(), key=lambda x: -x[1]):
        content += f"- {tech}: {count} projects\n"
    
    return content

def save_readme(content, filepath):
    """Save README content to file."""
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Saved: {filepath}")

def main():
    """Main processing function."""
    cx3_path = Path("/home/main/Documents/Hermes Agent Created Files/cx3")
    
    # Discover projects
    print("Discovering projects...")
    projects = discover_projects(cx3_path)
    
    if not projects:
        print("No projects discovered.")
        return
    
    print(f"Found {len(projects)} projects:")
    for project in projects:
        print(f"  - {project['name']}")
    
    # Generate platform-specific READMEs
    print("\nGenerating platform-specific READMEs...")
    
    # Web summary for portfolio
    web_readme = generate_web_readme(projects)
    save_readme(web_readme, cx3_path / "README_web.html")
    
    # GitHub README.md
    github_readme = generate_github_readme(projects)
    save_readme(github_readme, cx3_path / "README.md")
    
    # Concise summary README
    summary_readme = generate_summary_readme(projects)
    save_readme(summary_readme, cx3_path / "README_summary.md")
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()