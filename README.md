LabelKit

A lightweight web-based toolkit for reviewing, cleaning and managing YOLO-style image datasets.

LabelKit is a web-first dataset management tool designed to help developers efficiently review, deduplicate and manage image datasets with YOLO annotations.

It focuses on human-in-the-loop workflows rather than fully automated labeling.

✨ Features
✅ Dataset Review

Web-based image browser

YOLO bounding box visualization

Thumbnail preview with annotations

✅ Deduplication

Perceptual hash (pHash) based image similarity detection

Configurable similarity threshold

Automatic or manual staging of duplicate candidates

✅ Safe Deletion Workflow

Images are not deleted immediately

Deleted items are moved to a trash area

Changes are applied only after commit

✅ Commit & Rollback

Every delete operation creates a commit record

Full rollback support

Dataset history is preserved

✅ Clean Architecture

Web layer (app.py)

Business logic (services/)

Core algorithms (core/)

Easy to extend and test

📁 Project Structure
labelkit/
├── app.py                  # Flask web entry
├── config.py               # Global paths & config
│
├── services/               # Web-facing business logic
│   ├── dedup_service.py
│   ├── staging_service.py
│   ├── commit_service.py
│   └── draw_service.py
│
├── core/                   # Framework-agnostic logic
│   ├── dedup/
│   │   ├── phash.py
│   │   └── selector.py
│   └── yolo/
│       └── parser.py
│
├── data/
│   ├── images/
│   ├── labels/
│   ├── trash/
│   ├── staging.json
│   └── commits.json
│
└── templates/
    └── index.html

🚀 Getting Started
1. Install Dependencies
pip install flask pillow imagehash

2. Prepare Workspace
mkdir -p data/images data/labels


Put your images and YOLO .txt label files into the corresponding folders.

3. Run the Server
python app.py


Open your browser:

http://127.0.0.1:5000

🧠 Design Philosophy

Web-first: All dataset operations are done through the browser

Human-in-the-loop: Automated suggestions, manual decisions

Safety over speed: No irreversible operations without commit

Separation of concerns: Clean boundaries between Web / Service / Core

⚠️ Current Limitations

No in-browser box editing yet

No dataset version diff visualization

No authentication or multi-user support

UI is intentionally minimal

These are planned for future iterations.

🛣 Roadmap

 Web-based bounding box editing (LabelImg-style)

 More deduplication algorithms (SSIM / CLIP)

 Dataset version diff visualization

 Multi-dataset & multi-user support

 CLI support

🤝 Contributing

Contributions, issues and feature requests are welcome.

This project values:

Clean architecture

Explicit data flow

Practical dataset tooling

📄 License

MIT License

🙋 Why LabelKit?

LabelKit is built for developers who:

Work with large YOLO datasets

Need manual control over dataset quality

Want a lightweight alternative to full annotation platforms