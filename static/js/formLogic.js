document.addEventListener("DOMContentLoaded", function() {
    const sectionDependencies = {
        distortionContainer: {
            conditions: [
                () => document.querySelector('input[name="imageSource"]:checked')?.value === 'distorted',
            ],
        },
        hashingContainer: {
            conditions: [
                () => document.querySelector('#distortionContainer input[type="checkbox"]:checked') !== null,
            ],
        },
        graphContainer: {
            conditions: [
                () => document.querySelector('#hashingContainer input[type="checkbox"]:checked') !== null,
                () => document.querySelector('#distortionContainer input[type="checkbox"]:checked') !== null,
            ],
        },
        submitButtonContainer: {
            conditions: [
                () => document.querySelector('#graphContainer input[type="checkbox"]:checked') !== null,
                () => document.querySelector('#hashingContainer input[type="checkbox"]:checked') !== null,
                () => document.querySelector('#distortionContainer input[type="checkbox"]:checked') !== null,
            ],
        },
    };
    
    // Simplifying the updateSectionVisibility call
    function updateSectionVisibility() {
        Object.entries(sectionDependencies).forEach(([sectionId, dependency]) => {
            const section = document.getElementById(sectionId);
            // Check if all conditions are true for the section
            const shouldBeVisible = dependency.conditions.every(condition => condition());
    
            section.style.display = shouldBeVisible ? "block" : "none";
        });
    }
    fetch('/check-task-status')
    .then(response => response.json())
    .then(data => {
        if (!data.taskInProgress) {
            // No server-side task is in progress, so clear the flag
            localStorage.removeItem('taskInProgress');
            localStorage.removeItem('taskId');
            
            // Update UI as needed to reflect no task is in progress
        } else {
            // A task is in progress, maybe update UI accordingly
        }
    })
    .catch(error => console.error('Error fetching task status:', error));

    document.querySelectorAll('input[name="imageSource"]').forEach((elem) => {
        elem.addEventListener("change", function(event) {
            var value = event.target.value;
            var pathInput = document.getElementById("alreadyDistorted");
            var foldersContainer = document.getElementById("foldersContainer"); // Container for checkboxes

            if (pathInput) pathInput.style.display = value === "distorted" ? "block" : "none";
            if (foldersContainer) foldersContainer.innerHTML = ''; // Clear previous checkboxes

            if (value === "distorted") {
                fetch(`/get_folders/${value}`)
                .then(response => response.json())
                .then(folders => {
                    folders.forEach(folder => {
                        const wrapperDiv = document.createElement("div");
                        wrapperDiv.classList.add("checkbox-wrapper");

                        const checkbox = document.createElement("input");
                        checkbox.type = "checkbox";
                        checkbox.id = folder;
                        checkbox.name = "selectedFolders";
                        checkbox.value = folder;
                        checkbox.classList.add("first-form-checkbox");

                        const label = document.createElement("label");
                        label.htmlFor = folder;
                        label.textContent = folder;

                        wrapperDiv.appendChild(label);
                        wrapperDiv.appendChild(checkbox);

                        foldersContainer.appendChild(wrapperDiv);
                    });
                })
                .catch(error => console.error('Error fetching folders:', error));
            }
        });
        
    });

    function getAllCheckboxesNamedSelectedFolders() {
        // Use querySelectorAll to find all checkbox input elements with name="selectedFolders" inside the element with id="secondFormContainer"
        const checkboxes = document.querySelectorAll('#secondFormContainer input[type="checkbox"][name="subfolders"]');
        
        // Convert NodeList to an array for ease of use (if needed)
        const checkboxesArray = Array.from(checkboxes);
        
        return checkboxesArray;
    }

    document.getElementById('foldersContainer').addEventListener('change', function(event) {
        if (event.target.type === 'checkbox' && event.target.classList.contains('first-form-checkbox')) {
            const selectedFolders = Array.from(document.querySelectorAll('.first-form-checkbox:checked')).map(cb => cb.value);
            
            if (selectedFolders.length > 0) {
                fetch('/get-common-subfolders', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({selectedFolders}),
                })
                .then(response => response.json())
                .then(data => {
                    const secondFormContainer = document.getElementById('secondFormContainer');
                    if (secondFormContainer) secondFormContainer.innerHTML = ''; // Clear existing checkboxes

                    data.forEach(subfolder => {
                        const label = document.createElement('label');
                        label.textContent = subfolder;

                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.name = 'subfolders';
                        checkbox.value = subfolder;

                        label.prepend(checkbox);
                        secondFormContainer.appendChild(label);
                        secondFormContainer.appendChild(document.createElement('br'));
                    });
                    updateSectionVisibility(); 
                });
            }
        }
    });
    const submitButton = document.getElementById('submitAll');
    const statusMessage = document.getElementById('statusMessage') || createStatusMessage();

    function createStatusMessage() {
        const msg = document.createElement('div');
        msg.id = 'statusMessage';
        msg.style.display = 'none'; // Initially hidden
        document.body.appendChild(msg);
        return msg;
    }
    function checkTaskInProgress() {
        const allFormsContainer = document.querySelectorAll('imageSourceContainer');
        const submitButton = document.getElementById('submitAll');
        const statusMessage = document.getElementById('statusMessage') || createStatusMessage();
        fetch('/check-task-status')
            .then(response => response.json())
            .then(data => {

                // Update UI based on server response
                if (data.taskInProgress) {
                    allFormsContainer.forEach(form => form.style.display = 'none');
                    if (submitButton) submitButton.style.display = 'none';
                    statusMessage.style.display = 'block';
                    statusMessage.textContent = 'Processing... Please wait.';
                } else {
                    allFormsContainer.forEach(form => form.style.display = 'block');
                    if (submitButton) submitButton.style.display = 'block';
                    statusMessage.style.display = 'none';
                }
            })
            .catch(error => console.error('Error fetching task status:', error));
        fetch('/wait-for-task-completion')
            .then(response => response.json())
            .then(data => {
                console.log(data);
                allFormsContainer.forEach(form => form.style.display = 'block');
                if (submitButton) submitButton.style.display = 'block';
                if (statusMessage) statusMessage.style.display = 'none';
            })
            .catch(error => console.error('Error:', error));
    }
    function processFormData() {
        const allFormsContainer = document.querySelectorAll('.form-container');
        const allFormData = {
            imageSource: document.querySelector('input[name="imageSource"]:checked')?.value,
            selectedFolders: [],
            encodingTechniques: [],
            hashingTechniques: [],
            graphs: []
        };
        document.querySelectorAll('input[name="selectedFolders"]:checked').forEach(checkbox => {
            allFormData.selectedFolders.push(checkbox.value);
        });

        document.querySelectorAll('input[name="subfolders"]:checked').forEach(checkbox => {
            allFormData.encodingTechniques.push(checkbox.value);
        });
        document.querySelectorAll('input[name="hashing_techniques"]:checked').forEach(checkbox => {
            allFormData.hashingTechniques.push(checkbox.value);
        });
        document.querySelectorAll('input[name="graphs"]:checked').forEach(checkbox => {
            allFormData.graphs.push(checkbox.value);
        });

        localStorage.setItem('taskInProgress', 'true');
        allFormsContainer.forEach(form => form.style.display = 'none');
        if (submitButton) submitButton.style.display = 'none';
        if (statusMessage) {
            statusMessage.style.display = 'block';
            statusMessage.textContent = 'Processing... Please wait.';
        }

        fetch('/process-all', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(allFormData),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            localStorage.removeItem('taskInProgress');
            allFormsContainer.forEach(form => form.style.display = 'block');
            if (submitButton) submitButton.style.display = 'block';
            if (statusMessage) statusMessage.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            localStorage.removeItem('taskInProgress');
            allFormsContainer.forEach(form => form.style.display = 'block');
            if (submitButton) submitButton.style.display = 'block';
            if (statusMessage) statusMessage.style.display = 'none';
        });
    }
    function waitForTaskCompletion() {
        fetch('/wait-for-task-completion')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'completed') {
                    // Close the popup if you had one and continue processing
                    processFormData();
                }
            })
            .catch(error => {
                console.error('Error waiting for task completion:', error);
            });
    }
    document.getElementById('submitAll').addEventListener('click', function() {
        // Check if a task is already in progress
        fetch('/check-task-status')
            .then(response => response.json())
            .then(data => {
                if (data.taskInProgress) {
                    alert('A previous request is still being processed.');
                    // Optionally, wait for task completion before continuing
                    waitForTaskCompletion();
                } else {
                    processFormData();
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error checking task status:', error);
            });
    });

    document.getElementById('distortionContainer').addEventListener('change', (event) => {
        if (event.target.type === 'checkbox') {
            updateSectionVisibility();
        }
    });
    document.getElementById('hashingContainer').addEventListener('change', (event) => {
        if (event.target.type === 'checkbox') {
            updateSectionVisibility();
        }
    });
    document.getElementById('imageSourceContainer').addEventListener('change', (event) => {
        if (event.target.type === 'checkbox') {
            updateSectionVisibility();
        }
    });
    document.getElementById('graphContainer').addEventListener('change', (event) => {
        if (event.target.type === 'checkbox') {
            updateSectionVisibility();
        }
    });

    checkTaskInProgress();
});
