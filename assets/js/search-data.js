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
  },{id: "nav-publications",
          title: "Publications",
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
        },{id: "news-one-paper-accepted-by-ieee-transactions-on-vehicular-technology",
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
          section: "News",},{id: "news-one-paper-accepted-by-scientific-reports",
          title: 'One paper accepted by Scientific Reports.',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-by-pattern-recognition",
          title: 'One paper accepted by Pattern Recognition.',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-by-miccai-2026-workshop-sashimi",
          title: 'One paper accepted by MICCAI 2026 Workshop SASHIMI.',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-by-miccai-2026-workshop-mrixfields",
          title: 'One paper accepted by MICCAI 2026 Workshop MRIxFields.',
          description: "",
          section: "News",},{
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
