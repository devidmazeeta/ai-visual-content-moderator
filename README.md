# AI Visual Content Moderator

## 📂 Project Category
**Image Analysis**

## 📌 Description
**AI Visual Content Moderator** is a web-based application that automatically scans and moderates images using AI. It detects inappropriate content, identifies objects, recognizes scenes or landmarks, and extracts relevant tags and color themes. This tool is ideal for content moderation systems, social media platforms, and digital asset management.

---

## 🚀 Features

### 🧠 Object Detection
- Detects and identifies multiple objects within an image.
- Useful for content tagging, cataloging, and analysis.

### 🏷️ Image Tagging & Categorization
- Automatically generates descriptive tags based on image content.
- Categorizes images to support easy search and discovery.

### 🏞️ Scene & Landmark Recognition
- Recognizes natural and urban environments, landmarks, and structures.
- Enhances location-based content tagging.

### 🚫 Image Moderation
- Detects and flags explicit, violent, or inappropriate content.
- Supports safe and compliant image sharing on public platforms.

### 🎨 Color & Theme Extraction
- Extracts dominant colors and generates theme palettes.
- Useful for visual design analysis and media branding.

---

## 🌐 Use Cases
- Social media content moderation
- Automated image tagging for blogs and CMS
- Photo library organization
- Travel and location-based image sorting
- E-commerce image classification

---

## 🛠️ Tech Stack

- **Frontend**: HTML + CSS  
- **Backend**: Python (Flask)  
- **AI Services**: Azure AI Vision  
- **Storage**: MySQL  

---

## 📦 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-visual-content-moderator.git
   cd ai-visual-content-moderator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Configure your Azure AI Vision credentials.
   - Set MySQL connection strings in a `.env` file or config file.


4. **Run the application**
   ```bash
   python app.py
   ```

---

## 📸 Sample Input/Output
- Upload an image
- Get:  
  - Object labels  
  - Scene/landmark identification  
  - Tag suggestions  
  - Moderation status (Safe / Inappropriate)  
  - Dominant color palette

---

