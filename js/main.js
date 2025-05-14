document.addEventListener('DOMContentLoaded', function() {
    // Configure marked.js to handle math equations
    marked.setOptions({
        highlight: function(code, lang) {
            return code;
        }
    });

    // Fetch and display the folder structure
    fetchConversations();

    // Function to fetch conversations from the AI_Conversations directory
    function fetchConversations() {
        fetch('AI_Conversations/conversations.json')
            .then(response => response.json())
            .then(data => {
                renderFolderStructure(data);
            })
            .catch(error => {
                console.error('Error fetching conversations:', error);
                document.getElementById('folderList').innerHTML = '<p class="error">Error loading conversations. Please try again later.</p>';
            });
    }

    // Function to render the folder structure in the sidebar
    function renderFolderStructure(data) {
        const folderList = document.getElementById('folderList');
        folderList.innerHTML = '';

        Object.keys(data).forEach(folderName => {
            const folderDiv = document.createElement('div');
            folderDiv.className = 'folder';

            const folderTitle = document.createElement('div');
            folderTitle.className = 'folder-title';
            folderTitle.textContent = folderName;
            folderTitle.addEventListener('click', function() {
                const fileList = this.nextElementSibling;
                fileList.style.display = fileList.style.display === 'none' ? 'block' : 'none';
            });

            const fileList = document.createElement('div');
            fileList.className = 'file-list';

            // Create elements for each conversation file
            data[folderName].forEach(file => {
                Object.keys(file).forEach(subfolderName => {
                    const subfolder = document.createElement('div');
                    subfolder.className = 'folder';
                    
                    const subfolderTitle = document.createElement('div');
                    subfolderTitle.className = 'folder-title';
                    subfolderTitle.textContent = subfolderName;
                    subfolderTitle.style.fontSize = '0.9em';
                    subfolderTitle.addEventListener('click', function() {
                        const subfileList = this.nextElementSibling;
                        subfileList.style.display = subfileList.style.display === 'none' ? 'block' : 'none';
                    });
                    
                    const subfileList = document.createElement('div');
                    subfileList.className = 'file-list';
                    
                    file[subfolderName].forEach(conversation => {
                        const fileItem = document.createElement('div');
                        fileItem.className = 'file-item';
                        fileItem.textContent = conversation.name;
                        fileItem.dataset.path = conversation.path;
                        fileItem.addEventListener('click', function() {
                            // Set active class
                            document.querySelectorAll('.file-item').forEach(item => {
                                item.classList.remove('active');
                            });
                            this.classList.add('active');
                            
                            // Load conversation content
                            loadConversation(this.dataset.path);
                        });
                        
                        subfileList.appendChild(fileItem);
                    });
                    
                    subfolder.appendChild(subfolderTitle);
                    subfolder.appendChild(subfileList);
                    fileList.appendChild(subfolder);
                });
            });

            folderDiv.appendChild(folderTitle);
            folderDiv.appendChild(fileList);
            folderList.appendChild(folderDiv);
        });
    }

    // Function to load a conversation file
    function loadConversation(path) {
        fetch('/api/conversation?path=' + encodeURIComponent(path))
            .then(response => response.text())
            .then(markdown => {
                displayConversation(path, markdown);
            })
            .catch(error => {
                console.error('Error loading conversation:', error);
                document.getElementById('conversationContent').innerHTML = '<p class="error">Error loading conversation. Please try again later.</p>';
            });
    }

    // Function to display a conversation
    function displayConversation(path, markdown) {
        const contentDiv = document.getElementById('conversationContent');
        
        // Clear previous content
        contentDiv.innerHTML = '';
        
        // Add conversation title
        const filename = path.split('/').pop().replace('.md', '');
        const titleElement = document.createElement('h2');
        titleElement.className = 'conversation-title';
        titleElement.textContent = filename;
        contentDiv.appendChild(titleElement);

        // Parse the markdown and render each section
        const sections = parseConversationSections(markdown);
        sections.forEach(section => {
            const sectionDiv = document.createElement('div');
            sectionDiv.className = section.type;
            
            const titleElement = document.createElement('h3');
            titleElement.textContent = section.title;
            sectionDiv.appendChild(titleElement);
            
            const contentElement = document.createElement('div');
            contentElement.className = 'section-content';
            contentElement.innerHTML = marked.parse(section.content);
            sectionDiv.appendChild(contentElement);
            
            contentDiv.appendChild(sectionDiv);
        });
    }

    // Function to parse conversation sections
    function parseConversationSections(markdown) {
        const sections = [];
        const lines = markdown.split('\n');
        
        let currentSection = null;
        let currentContent = [];
        
        lines.forEach(line => {
            if (line.startsWith('### User Prompt')) {
                // Save previous section if exists
                if (currentSection) {
                    sections.push({
                        type: currentSection.includes('User') ? 'prompt' : 'answer',
                        title: currentSection,
                        content: currentContent.join('\n')
                    });
                }
                
                // Start new user section
                currentSection = line.substring(4).trim();
                currentContent = [];
            } else if (line.startsWith('### Gemini')) {
                // Save previous section if exists
                if (currentSection) {
                    sections.push({
                        type: currentSection.includes('User') ? 'prompt' : 'answer',
                        title: currentSection,
                        content: currentContent.join('\n')
                    });
                }
                
                // Start new AI section
                currentSection = line.substring(4).trim();
                currentContent = [];
            } else if (line.trim() === '---') {
                // Ignore separator lines
                return;
            } else {
                // Add to current content
                currentContent.push(line);
            }
        });
        
        // Add the last section
        if (currentSection) {
            sections.push({
                type: currentSection.includes('User') ? 'prompt' : 'answer',
                title: currentSection,
                content: currentContent.join('\n')
            });
        }
        
        return sections;
    }
}); 
