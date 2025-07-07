# Use linux Tree command to communicate your folder structure to your LLM

You can use `tree` to create a tree ASCII structure for your folder and paste it to your LLM window. However it is sometimes neccessary to ignore some folders by using `tree -I` 

For example ` tree -I "node_modules| components" ` ignores node_modules and components forlders. Below is an example output 

`bash
          .

├── chess

│   ├── chess-coach

│   │   ├── README.md

│   │   ├── eslint.config.js

│   │   ├── index.html

│   │   ├── package-lock.json

│   │   ├── package.json

│   │   ├── postcss.config.cjs

│   │   ├── public

│   │   │   ├── stockfish.js

│   │   │   └── vite.svg

│   │   ├── src

│   │   │   ├── App.css

│   │   │   ├── App.jsx

│   │   │   ├── assets

│   │   │   │   └── react.svg

│   │   │   ├── index.css

│   │   │   ├── main.jsx

│   │   │   └── puzzles.js

│   │   ├── tailwind.config.cjs

│   │   └── vite.config.js

│   ├── icon.html

│   ├── prompt.md

│   └── readme.md

├── chess_coach.mp4

├── lichess_db_puzzle.csv

└── puzzles.csv
`
