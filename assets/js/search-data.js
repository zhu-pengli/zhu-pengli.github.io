// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-home",
    title: "Home",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-selected-publications",
          title: "Selected Publications",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-curriculum-vitae",
          title: "Curriculum Vitae",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "books-the-godfather",
          title: 'The Godfather',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/the_godfather/";
            },},{id: "news-one-paper-accepted-by-ieee-transactions-on-vehicular-technology",
          title: 'One paper accepted by IEEE Transactions on Vehicular Technology.',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-by-applied-intelligence",
          title: 'One paper accepted by Applied Intelligence.',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-by-journal-of-visual-communication-and-image-representation",
          title: 'One paper accepted by Journal of Visual Communication and Image Representation.',
          description: "",
          section: "News",},{id: "news-two-paper-accepted-by-oceans-2024-singapore-and-selected-for-oral-presentation",
          title: 'Two paper accepted by OCEANS 2024-Singapore and selected for oral presentation.',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-by-ieee-journal-of-oceanic-engineering",
          title: 'One paper accepted by IEEE Journal of Oceanic Engineering.',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-by-engineering-applications-of-artificial-intelligence",
          title: 'One paper accepted by Engineering Applications of Artificial Intelligence.',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-by-medical-image-analysis",
          title: 'One paper accepted by Medical Image Analysis.',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-by-miccai-2025-early-accepted-top-9",
          title: 'One paper accepted by MICCAI 2025, early accepted (top 9%).',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-by-ieee-transactions-on-pattern-analysis-and-machine-intelligence",
          title: 'One paper accepted by IEEE Transactions on Pattern Analysis and Machine Intelligence.',
          description: "",
          section: "News",},{id: "news-awarded-1st-prize-in-the-brain-region-segmentation-task-of-the-parkinson-s-disease-auto-diagnosis-challenge-miccai-2025",
          title: 'Awarded 1st Prize in the Brain Region Segmentation Task of the Parkinson’s Disease...',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-by-ieee-transactions-on-medical-imaging",
          title: 'One paper accepted by IEEE Transactions on Medical Imaging.',
          description: "",
          section: "News",},{id: "projects-project-1",
          title: 'project 1',
          description: "with background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_project/";
            },},{id: "projects-project-2",
          title: 'project 2',
          description: "a project with a background image and giscus comments",
          section: "Projects",handler: () => {
              window.location.href = "/projects/2_project/";
            },},{id: "projects-project-3-with-very-long-name",
          title: 'project 3 with very long name',
          description: "a project that redirects to another website",
          section: "Projects",handler: () => {
              window.location.href = "/projects/3_project/";
            },},{id: "projects-project-4",
          title: 'project 4',
          description: "another without an image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/4_project/";
            },},{id: "projects-project-5",
          title: 'project 5',
          description: "a project with a background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/5_project/";
            },},{id: "projects-project-6",
          title: 'project 6',
          description: "a project with no image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/6_project/";
            },},{id: "projects-project-7",
          title: 'project 7',
          description: "with background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/7_project/";
            },},{id: "projects-project-8",
          title: 'project 8',
          description: "an other project with a background image and giscus comments",
          section: "Projects",handler: () => {
              window.location.href = "/projects/8_project/";
            },},{id: "projects-project-9",
          title: 'project 9',
          description: "another project with an image 🎉",
          section: "Projects",handler: () => {
              window.location.href = "/projects/9_project/";
            },},{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
