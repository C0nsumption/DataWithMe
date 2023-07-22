📊 DataWithMe
A small social platform dedicated to the posting, analyzing, and discussing of data. 📈 Here, you'll find an overview of the current features and progress. For details on upcoming features and updates, feel free to check the pull requests.

Goals:
```
✅ Flask Backend
✅ Vue.js Based Client
✅ SQLite Database
❌ ChatGPT API intergration
```

## 🚀 **Notable Feature Additions:**

- ### 🔐 Configuration Management
    Environment variables have been integrated for configuration management. This encompasses:
    - Addition of `.env` files.
    - Usage of `python-dotenv`.
    - Transferring sensitive data to environment variables.

- ### 🛡️ Security Enhancements
    - Improved password hashing using Werkzeug's security module.

- ### ✅ Testing with Pytest
    - Integrated Pytest for efficient application testing.
    - Tests written for all current application routes.

- ### 📝 User and Post Functionality
    - Expansion in routes to delete both users and posts.
    - Integrated testing for these new functionalities.

- ### 👤 User Profile Experience
    - Overhauled the user experience on the client-side.
    - Enhanced profile viewing and post interaction capabilities.
    - Introduced confirmation prompts for post deletions.

- ### 🚪 Logout System
    - Implemented a comprehensive logout system with state management for the JWT token.

- ### 🔍 User Search System
    - Search functionality for users, supported by a Vue component.

- ### 🌐 Authentication and Profile Enhancement
    - Separated login and sign-up forms.
    - Enhanced user profiles with 'bio', 'profile_photo', and potential following system.

- ### 👁️ Profile Viewing
    - Modal-based system for user profiles after a search.
    - Distinct components for own vs. others' profiles.

- ### 📜 Other Users' Posts
    - Ability to view posts from other users on their profile pages.

## 🌱 **Upcoming Features**
1. Integration of the ChatGPT API.
2. Further UI/UX enhancements.
3. Potential optimization of the following system.

> 🔔 **Tip:** Remember to check the pull requests for insights into what's being worked on. Contributions and feedback are always welcome!

---

📖 "Getting Started" and "How to Contribute" sections coming soon. Project is still in its early stages.
