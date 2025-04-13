#Samuel Schuur, 2023
import re

class ResumeComponent:
	"""Base class for resume components."""

	def format_link(self, text):
		# Replace markdown links with HTML links
		text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
		# Replace markdown newlines with HTML newlines
		text = re.sub(r'\n\n|\n(?=\s)', '<br>', text)
		return text

	def add_description(self, description):
		self.description = self.format_link(description)
		return self

	def render(self):
		title = self.render_title()
		content = self.render_content()
		return f'<div class="row"><div class="title">{title}</div><div class="content">{content}</div></div>'	

	def render_title(self):
		return ""

	def render_content(self):
		return ""

class Job(ResumeComponent):
	def __init__(self, title, company, start, end=None, description=None):
		super().__init__()
		self.title = title
		self.company = self.format_link(company)
		self.start = start
		self.end = end
		self.description = self.format_link(description) if description else ""

	def render_title(self):
		#dates go here; two cases w/ and w/o end date
		if self.end:
			return f"{self.start} - {self.end}"
		else:
			return f"{self.start}"

	def render_content(self):
		#put title in bold then company then description
		return f"<b>{self.title}</b> at <b>{self.company}</b> <br>{self.description}"

	def render_multicontent(self):
		#same as render_content but without company
		return f"<b>{self.start}, {self.title}</b> {self.description}<br><br>"

class MultiJob(ResumeComponent):
	def __init__(self, jobs=None, description=None):
		super().__init__()
		self.description = self.format_link(description) if description else ""
		self.description = f"<b>{self.description}</b>"
		self.jobs = jobs if jobs else []

	def add_job(self, job):
		self.jobs.append(job)
		return self

	def render_title(self):
		#dates go here: two cases last job has end date and last job doesn't have end date
		if self.jobs[-1].end:
			return f"{self.jobs[0].start} - {self.jobs[-1].end}"
		else:
			return f"{self.jobs[0].start} - {self.jobs[-1].start}"

	def render_content(self):
		#put description if it exists then each job using render_multicontent
		if self.description:
			return f"{self.description}<br><br>{''.join(job.render_multicontent() for job in self.jobs)}"
		else:
			return f"{''.join(job.render_multicontent() for job in self.jobs)}"

class Education(ResumeComponent):
	def __init__(self, school, start, end, description=None):
		super().__init__()
		self.school = school
		self.start = start
		self.end = end
		self.description = self.format_link(description) if description else ""

	def render_title(self):
		#dates, 2 cases w/ and w/o end date
		if self.end:
			return f"{self.start} - {self.end}"
		else:
			return f"{self.start}"

	def render_content(self):
		#school in bold then description
		return f"<b>{self.school}</b> {self.description}"

class Skill(ResumeComponent):
	def __init__(self, skill, description=None):
		super().__init__()
		self.skill = skill
		self.description = self.format_link(description) if description else ""

	def render_title(self):
		return f"{self.skill}"

	def render_content(self):
		return f"{self.description}"

class Divider(ResumeComponent):
	"""class for dividers between sections, redefines render"""
	def __init__(self, title):
		super().__init__()
		self.title = title

	def render(self):
		#we render titles as h3s
		return f"<h3>{self.title}</h3>"

class Work(ResumeComponent):
    """Class to represent a single work entry."""
    def __init__(self, publication, paper_title):
        super().__init__()
        self.publication = self.format_link(publication)
        self.paper_title = self.format_link(paper_title)

    def render_title(self):
        # Left column: Publication
        return f"{self.publication}"

    def render_content(self):
        # Right column: Paper Title
        return f"{self.paper_title}"

class BasePage:
    """Base class for shared rendering logic between Resume and Portfolio."""
    def __init__(self, name, email, description=None):
        self.name = name
        self.email = email
        self.description = self.format_link(description) if description else ""

    def format_link(self, text):
        # Replace markdown links with HTML links
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
        # Replace markdown newlines with HTML newlines
        text = re.sub(r'\n\n|\n(?=\s)', '<br>', text)
        return text

    def render_header(self):
        return """
        <!doctype html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>samuel schuur</title>
        <link rel="stylesheet" href="https://use.typekit.net/cse0ubf.css">
        <link rel="icon" href="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><rect width='8' height='16' fill='%23C46A0D'/><rect x='8' width='8' height='16' fill='%23A39B90'/></svg>" type="image/svg+xml">
        <style>
            body {
                font-family: 'maiola', serif;
                font-size: 15px;
                width: 500px;
            }
            h1 {
                font-family: 'p22-underground', sans-serif;
                font-size: 20px;
                color: #C46A0D;
            }
            h2 {
                font-family: 'p22-underground', sans-serif;
                font-size: 17px;
                color: #A39B90;
            }
            h1, h2 {
                margin-top: 2px;
                margin-bottom: 2px;
            }
            h2 a {
                color: #C46A0D; /* Orange color for links */
                text-decoration: none;
            }
            h2 a:hover {
                color: #A39B90; /* Gray color on hover */
            }
            a {
                color: #C46A0D; /* Orange color for all links */
                text-decoration: none;
            }
            a:hover {
                color: #A39B90; /* Gray color on hover */
            }
            h3 {
                font-family: 'p22-underground', sans-serif;
                font-size: 15px;
                color: #A39B90;
                border-bottom: 1px solid;
            }
            .row {
                display: flex;
                justify-content: space-between;
            }
            .title {
                flex-basis: 0;
                flex-grow: 1;
                padding: 5px;
                font-style: italic;
                text-align: right; /* Right-align the title column */
            }
            .content {
                flex-basis: 0;
                flex-grow: 3;
                padding: 5px;
                padding-left: 10px;
                margin-left: 0;
            }
            .carousel {
                position: relative;
                width: 100%;
                overflow: hidden;
            }

            .carousel img {
                width: 100%;
                display: block;
            }

            .carousel-overlay {
                position: absolute;
                top: 0;
                bottom: 0;
                width: 50%;
                cursor: pointer;
                z-index: 10;
            }

            .carousel-overlay.left {
                left: 0;
                cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="%23C46A0D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>') 12 12, w-resize;
            }

            .carousel-overlay.right {
                right: 0;
                cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="%23C46A0D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>') 12 12, e-resize;
            }
        </style>
        </head>
        <body>
        """

    def render_footer(self):
        return """
        <footer style="text-align: center; font-family: 'p22-underground', sans-serif; font-size: 12px; color: #A39B90; margin-top: 20px;">
            s. schuur, 2025
        </footer>
        </body>
        </html>
        """

    def render_common_section(self):
        return f"""
        <h1>{self.name}</h1>
        <h2>{self.email}</h2>
        <p>{self.description}</p>
        <h2><a href="index.html">Resume</a>, <a href="portfolio.html">Portfolio</a></h2>
        """


class Resume(BasePage):
    def __init__(self, name, email, description=None):
        super().__init__(name, email, description)
        self.jobs = []
        self.education = []
        self.skills = []
        self.works = []  # New list for work entries

    def add_job(self, job):
        self.jobs.append(job)
        return self

    def add_education(self, education):
        self.education.append(education)
        return self

    def add_skill(self, skill):
        self.skills.append(skill)
        return self

    def add_work(self, work):
        self.works.append(work)
        return self

    def render(self):
        # Render individual sections
        jobs_html = ''.join(job.render() for job in self.jobs)
        education_html = ''.join(education.render() for education in self.education)
        skills_html = ''.join(skill.render() for skill in self.skills)
        works_html = ''.join(work.render() for work in self.works)

        # Create dividers with labels
        jobs_divider = Divider("Experience").render()
        education_divider = Divider("Education").render()
        skills_divider = Divider("Skills").render()
        works_divider = Divider("Work").render()  # New divider for work section

        # Construct the final HTML
        html_parts = [
            self.render_header(),
            self.render_common_section(),
            education_divider,
            education_html,
            jobs_divider,
            jobs_html,
            skills_divider,
            skills_html,
            works_divider,  # Add the work section
            works_html,
            self.render_footer()
        ]
        return ''.join(html_parts)


class PortfolioEntry:
    """Class to represent a single portfolio entry."""
    def __init__(self, title, description, images, formatter):
        self.title = title
        self.description = formatter.format_link(description)  # Use the formatter's format_link method
        self.images = images  # List of image URLs

    def render(self):
        # Render the title using the Divider class
        title_html = Divider(self.title).render()

        # Render the image carousel
        carousel_id = self.title.replace(" ", "_").lower()  # Unique ID for the carousel
        images_html = f"""
        <div class="carousel" id="{carousel_id}" style="position: relative; width: 100%; overflow: hidden;">
            <img src="{self.images[0]}" alt="{self.title}" class="carousel-image" style="width: 100%; display: block;">
            <div class="carousel-overlay left" onclick="prevImage('{carousel_id}')"></div>
            <div class="carousel-overlay right" onclick="nextImage('{carousel_id}')"></div>
        </div>
        """

        # Add JavaScript for the carousel
        script_html = f"""
        <script>
        window['{carousel_id}_images'] = {self.images};
        window['{carousel_id}_index'] = 0;

        function nextImage(carouselId) {{
            const images = window[carouselId + '_images'];
            let index = window[carouselId + '_index'];
            index = (index + 1) % images.length;
            window[carouselId + '_index'] = index;
            document.querySelector('#' + carouselId + ' .carousel-image').src = images[index];
        }}

        function prevImage(carouselId) {{
            const images = window[carouselId + '_images'];
            let index = window[carouselId + '_index'];
            index = (index - 1 + images.length) % images.length;
            window[carouselId + '_index'] = index;
            document.querySelector('#' + carouselId + ' .carousel-image').src = images[index];
        }}
        </script>
        """

        # Render the description
        description_html = f'<p>{self.description}</p>'

        # Combine all parts
        return f'{title_html}{images_html}{description_html}{script_html}'


class Portfolio(BasePage):
    def __init__(self, name, email, description=None):
        super().__init__(name, email, description)
        self.entries = []  # List of PortfolioEntry objects

    def add_entry(self, title, description, images):
        # Pass self (the Portfolio instance) as the formatter
        self.entries.append(PortfolioEntry(title, description, images, self))
        return self

    def render(self):
        # Render portfolio-specific content
        portfolio_content = ""
        for entry in self.entries:
            portfolio_content += entry.render()

        # Construct the final HTML
        html_parts = [
            self.render_header(),  # Use the BasePage render_header method
            self.render_common_section(),
            portfolio_content,
            self.render_footer()
        ]
        return ''.join(html_parts)


# Define shared variables for name and email
name = "samuel schuur"
email = "schuursamuel at gmail dot com"

header = "Hi, I'm samuel schuur, a student at the University of Chicago studying maths. Previously I've worked at the Center for Bits and Atoms at MIT, building tools for flexible computing and manufacturing workflows, as well as at Elmworks in Berkeley, CA developing wire plotting tools for building high frequency electromagnetic devices. I enjoy complex linkages and precision machine design. In my free time I build furniture, and combat robots. I also play the violin."

# Create resume instance
resume = Resume(name=name, email=email, description=header)

# Add education, jobs, and skills to the resume
resume.add_education(Education(
    school="University of Chicago",
    start="2022",
    end="expected 2026",
    description="Mathematics, Architectural Studies"
))

resume.add_education(Education(
    school="Gap year",
    start="2022",
    end=None,
    description="audited MIT 6.004 Computational Structures, MIT 6.849 GFALOP (async lectures), MIT 22.061 Fusion Energy, MITERS keyholder"
))

resume.add_education(Education(
    school="Horace Mann School",
    start="2015",
    end="2021",
    description="High School Diploma"
))

resume.add_job(Job(
	title = "Suspension Lead",
	start="January  2025",
	company = "UChicago FSAE"
	))

resume.add_job(Job(
		title="Participant",
		start="June 2024",
		company="Design Assembly",
		description="Worked to hand draft and build a trussed boat storage shed with a team of students in a remote location."
	))

resume.add_job(Job(
	title="Student Researcher",
	company="Enrico Fermi Institute",
	start="2023",
	description="Frisch Group"
))

mitmulti = MultiJob(description="the Center for Bits and Atoms")

mitmulti.add_job(Job(
    title="Intern",
    company="Center for Bits and Atoms",
    start="Summer 2023",
    description="Worked to develop instrumented CNC tools for the NIST Materials Genome Project, also helped test drive new modular motion planning systems by developing specialty tools (and interfaces for them) for precreasing origami in conjunction with the MIT museum."
))

mitmulti.add_job(Job(
    title="Machine Development Specialist",
    company="Center for Bits and Atoms",
    start="2022",
    description="Built tools for flexible computing and manufacturing workflows in association with AFRL."
))

mitmulti.add_job(Job(
    title="Intern",
    company="Center for Bits and Atoms",
    start="Summer 2020",
    description="Worked for the Machines that Make project, testing and assembling kits for the remote edition of 'How To Make (almost) Anything,' also developed custom extruder toolheads for said machines."
))

mitmulti.add_job(Job(
    title="Intern",
    company="Center for Bits and Atoms",
    start="Summer 2019",
    description="Worked on the Machines that Make project; assembled and wired custom gantry based machines, developed a 3d printed tool changing system."
))

# Add mitmulti to the resume
resume.add_job(mitmulti)

resume.add_job(Job(
	title="Intern",
	company="Elmworks",
	start="Sep 2021",
	end="Jan 2022",
	description="Worked on custom wire plotting tools for building high frequency electromagnetic devices doing both mechanical and electrical design and testing!"
))

resume.add_skill(Skill(
	skill = "Programming",
	description  ="Python, Java, Javascript, C++, systems level C, as well as some assembly (x86, riscV)"
	))

resume.add_skill(Skill(
	skill = "Manufacturing",
	description = "Extrensive CAD and CAM experience, as well as CNC and manual machining, including mills, lathes, waterjets, EDM's, and metal lasers"
	))

resume.add_skill(Skill(
	skill = "Electronics",
	description = "PCB design and layout in Altium and Kicad, SMD soldering and assembly"
	))

# Add work entries to the resume


resume.add_work(Work(
    publication="Integrating Materials and Manufacturing Innovation",
    paper_title="Online Measurement for Parameter Discovery in Fused Filament Fabrication"
))
# Render the resume
html_resume = resume.render()

# Write the resume to a file
with open("index.html", "w") as f:
	f.write(html_resume)

# Create portfolio instance
portfolio = Portfolio(name=name, email=email, description=header)

# Add portfolio entries
portfolio.add_entry(
    title="Combat Robotics",
    description='In my free time I enjoy building combat robots which I have competed with at NHRL and smaller events. Frankly, I enjoy the design and manufacturing of these robots more than actually competing with them (though of course that\'s also enjoyable) and as a result I think my bots have ended up with all sorts of interesting design features and weird compact packaging. I currently am working on a 3lb and a 30lb bot both with drive motors packaged coaxially with the wheels and shock isolated direct drive "hub motor" weapons. Both are abnormally compact for their respective weight classes. I also am working on a 12lb pneumatic flipper with a completely custom air system - but that got sidetracked by me going down a rabbit hole of high airflow valve design!',
    images=["images/robots/flycut.jpg", "images/robots/cruft.jpg", "images/robots/flycut2.jpg", "images/robots/cruftwep.jpg", "images/robots/ncrawlerdrive.jpg", "images/robots/frame.jpg", "images/robots/flycut2wheels.jpg", "images/robots/airtank.jpg"]
)

portfolio.add_entry(
    title="Origami Tools",
    description="As a personal offshoot from my work at the Center for Bits and Atoms stemming from my interest in computation geometry and the mathematics underlying origami I have worked on a series of CNC tools for precreasing complex origami patterns as a testing platform for new modular motion control systems. These machines have been shown at the MIT museum which is neat! This project also led me down a rabbit hole of paper metrology at one point which I devised some strange testing rigs, I also learned more then I could ever have wanted to about how SVG files work in writing their control software. You can see an old video of one of my precreasing machines here: [https://www.youtube.com/watch?v=nkSGZQBx5p4](https://www.youtube.com/watch?v=nkSGZQBx5p4)",
    images=["images/origami/origamachine.jpg", "images/origami/origamachine2.jpg", "images/origami/origamisoftware.jpg", "images/origami/creasingtools.jpg"]
)

portfolio.add_entry(
    title="Furniture",
    description="In my free time I also enjoy designing and building furniture - I have designed a couple desks generated from parametric CAD files and cut out of flat sheets of plywood. I've also built a small adjustable climbing wall for my living room! I'm currently working on a plywood and folded sheet metal bench for my room.",
    images=["images/furniture/desks.jpg", "images/furniture/computerdesk.jpg", "images/furniture/climbingwall.jpg"]
)

portfolio.add_entry(
    title="Misc",
    description="In general I just like designing and making things with my hands! I've worked on all sorts of other random projects:  machined pens, bike lights with fun custom fresnel lenses, clocks, strange belt reductions, cast wheels, to just hand polishing bike parts, etc.",
    images=["images/misc/pen.jpg", "images/misc/light.jpg", "images/misc/machining.jpg", "images/misc/clock.jpg", "images/misc/belts.jpg", "images/misc/wheels.jpg"]
)

# Render the portfolio
html_portfolio = portfolio.render()

# Write the portfolio to a file
with open("portfolio.html", "w", encoding="utf-8") as f:
    f.write(html_portfolio)