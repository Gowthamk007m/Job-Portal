// close alerts after on clicking
document.addEventListener('DOMContentLoaded', function() {
  const closeButtons = document.querySelectorAll('.custom-close');

  closeButtons.forEach(button => {
    button.addEventListener('click', function() {
      const alert = this.closest('.custom-alert');
      if (alert) {
        alert.classList.add('closing');
      }
    });
  });
});

// Pagination Js
let currentPage = document.querySelector('.page-item.active');

if (currentPage) {
    let currentPageNum = parseInt(currentPage.querySelector('a').innerText);
    let totalPages = document.querySelectorAll('#pagination .count-page').length;

    const pagesToShow = 2;

    let pages = document.querySelectorAll('#pagination .page-item');
    pages.forEach(page => page.style.display = 'none');

    let startPage;
    if (currentPageNum === 1) {
        startPage = 1;
    } else if (currentPageNum === 2) {
        startPage = 1;
    } else if (currentPageNum === totalPages) {
        startPage = Math.max(1, currentPageNum - 4);
    } else if (currentPageNum === totalPages - 1) {
        startPage = Math.max(1, currentPageNum - 3);
    } else {
        startPage = Math.max(1, currentPageNum - pagesToShow);
    }

    let endPage = Math.min(totalPages, startPage + 4);

    if (endPage - startPage + 1 < 5) {
        startPage = Math.max(1, endPage - 4);
    }

    for (let i = startPage; i <= endPage; i++) {
        let pageToShow = document.querySelector(`#pagination .page-item:nth-child(${i + 1})`);
        if (pageToShow) {
            pageToShow.style.display = 'block';
        }
    }

    document.getElementById('prevPage').style.display = 'block';
    document.getElementById('nextPage').style.display = 'block';

    if (currentPageNum === 1) {
        document.getElementById('prevPage').classList.add('disabled');
        document.getElementById('prevPage').querySelector('a').setAttribute('aria-disabled', 'true');
    } else {
        document.getElementById('prevPage').classList.remove('disabled');
        document.getElementById('prevPage').querySelector('a').removeAttribute('aria-disabled');
    }

    if (currentPageNum === totalPages) {
        document.getElementById('nextPage').classList.add('disabled');
        document.getElementById('nextPage').querySelector('a').setAttribute('aria-disabled', 'true');
    } else {
        document.getElementById('nextPage').classList.remove('disabled');
        document.getElementById('nextPage').querySelector('a').removeAttribute('aria-disabled');
    }
}


// Multi Select Search Box
document.addEventListener('DOMContentLoaded', function() {
    function setupSearchInput(selectId, placeholderText) {
        var selectElement = document.getElementById(selectId);
        if (!selectElement) return;

        var searchInput = document.createElement('input');
        searchInput.setAttribute('type', 'text');
        searchInput.setAttribute('class', 'form-control mb-2');
        searchInput.setAttribute('placeholder', placeholderText);

        var formGroup = selectElement.closest('.form-group');
        if (!formGroup) return;

        formGroup.insertBefore(searchInput, selectElement);

        searchInput.addEventListener('input', function() {
            var searchText = this.value.toLowerCase();
            var options = selectElement.querySelectorAll('option');

            options.forEach(function(option) {
                var optionText = option.textContent.toLowerCase();
                if (optionText.includes(searchText)) {
                    option.style.display = 'block';
                } else {
                    option.style.display = 'none';
                }
            });
        });
    }

    // Usage without error messages
    setupSearchInput('id_interests', 'Search interests');
    setupSearchInput('id_hobbies', 'Search hobbies');
});


// select Search
function initializeSelectSearchByIds(selectIds, noResultButtonIds, fetchjobtitlesIds) {
    document.addEventListener("DOMContentLoaded", function() {
        const selectElements = {};

        selectIds.forEach(function(selectId) {
            const selectElement = document.getElementById(selectId);

            if (selectElement) {
                selectElements[selectId] = selectElement;

                // Hide the select element
                selectElement.style.display = "none";

                // Create search input
                const searchInput = document.createElement("input");
                searchInput.type = "text";
                searchInput.id = `${selectId}Search`;
                searchInput.classList.add("form-control", "mb-2");
                searchInput.placeholder = `Search in ${selectElement.getAttribute('name') || 'options'}...`;

                // Create div for displaying search results
                const searchResultsDiv = document.createElement("div");
                searchResultsDiv.id = `${selectId}Results`;
                searchResultsDiv.classList.add("search-results");
                searchResultsDiv.style.display = "none"; // Initially hidden

                // Insert search input and results div before the select element
                selectElement.parentNode.insertBefore(searchInput, selectElement);
                selectElement.parentNode.insertBefore(searchResultsDiv, selectElement);

                function filterOptions(searchText) {
                    searchResultsDiv.innerHTML = ''; // Clear previous results
                    let resultsFound = true;
                    const options = Array.from(selectElement.options);

                    options.forEach(function(option) {
                        const optionText = option.textContent.toLowerCase();
                        if (optionText.includes(searchText.toLowerCase())) {
                            const optionDiv = document.createElement("div");
                            optionDiv.textContent = option.textContent;
                            optionDiv.classList.add("search-option");
                            optionDiv.dataset.value = option.value;

                            optionDiv.addEventListener("click", function() {
                                selectElement.value = optionDiv.dataset.value;
                                searchInput.value = optionDiv.textContent;
                                searchResultsDiv.innerHTML = ''; // Clear results
                                searchResultsDiv.style.display = "none";
                                updatePlaceholder(); // Update placeholder after selection
                            });

                            searchResultsDiv.appendChild(optionDiv);
                            resultsFound = true;
                        }
                    });

                    // Add the button as the last child if applicable
                    if (fetchjobtitlesIds.includes(selectId)) {
                        const button = document.createElement("button");
                        button.type = "button";
                        button.id = "open-modal-button";
                        button.classList.add("btn", "btn-secondary", "w-100");
                        button.textContent = "Add New Job Title";
                        button.setAttribute("data-bs-toggle", "modal");
                        button.setAttribute("data-bs-target", "#addJobTitleModal");
                        searchResultsDiv.appendChild(button);
                    }

                    // Show or hide the results div
                    if (searchText.trim() === '') {
                        searchResultsDiv.style.display = "none";
                    } else {
                        searchResultsDiv.style.display = resultsFound || noResultButtonIds.includes(selectId) ? "block" : "none";
                    }
                }

                function updatePlaceholder() {
                    const selectedOption = selectElement.options[selectElement.selectedIndex];
                    if (selectedOption) {
                        searchInput.placeholder = selectedOption.textContent;
                    } else {
                        searchInput.placeholder = `Search in ${selectElement.getAttribute('name') || 'options'}...`;
                    }
                }

                searchInput.addEventListener("input", function() {
                    const searchText = searchInput.value.trim();
                    filterOptions(searchText);
                });

                selectElement.addEventListener("change", function() {
                    updatePlaceholder(); // Update placeholder when selection changes
                    const selectedOption = selectElement.options[selectElement.selectedIndex];
                    if (selectedOption) {
                        searchInput.value = selectedOption.text;
                        filterOptions(searchInput.value);
                    }
                });

                // Set initial placeholder and value
                const selectedOption = selectElement.options[selectElement.selectedIndex];
                if (selectedOption) {
                    searchInput.placeholder = selectedOption.text;
                    updatePlaceholder();
                } else {
                    searchInput.placeholder = `Search in ${selectElement.getAttribute('name') || 'options'}...`;
                }
                filterOptions(''); // Display all options initially
            }
        });

        // Function to fetch and update options from the server
        window.fetchOptions = function() {
            fetchjobtitlesIds.forEach(function(selectId) {
                const selectElement = selectElements[selectId];
                if (selectElement) {
                    fetch(`/job-profile/job-titles/`) // Adjust the URL based on your setup
                        .then(response => response.json())
                        .then(data => {
                            const previousLength = selectElement.options.length;
                            selectElement.innerHTML = ''; // Clear existing options

                            data.forEach(function(option) {
                                const newOption = new Option(option.title, option.id);
                                selectElement.add(newOption);
                            });

                            // Re-filter the options if the input has a value
                            const searchInput = document.getElementById(`${selectId}Search`);
                            if (searchInput) {
                                const searchText = searchInput.value.trim();
                                if (searchText) {
                                    filterOptions(searchText);
                                    searchResultsDiv.style.display = "block";
                                }
                            }

                            // Automatically show results if new options are added and search input is not empty
                            if (previousLength < selectElement.options.length) {
                                const searchInput = document.getElementById(`${selectId}Search`);
                                if (searchInput) {
                                    const searchText = searchInput.value.trim();
                                    if (searchText) {
                                        filterOptions(searchText);
                                    }
                                }
                            }
                        })
                        .catch(error => console.error('Error fetching options:', error));
                }
            });
        }
    });
}

// Usage
initializeSelectSearchByIds(["id_skill", "id_job_title", "id_location", "id_title", "id_company"], ["id_title", "id_job_title"], ["id_title", "id_job_title"]);

// jQuery code for handling the modal and adding job titles
$(document).ready(function() {
    // Set CSRF token for AJAX requests
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

    $('#open-modal-button').click(function() {
        $('#addJobTitleModal').modal('show');
    });

    $('#add-job-title').click(function() {
        var newTitle = $('#new-job-title').val().trim();
        if (newTitle) {
            $.ajax({
                url: jobtitleaddUrl, // Ensure this URL is correctly set
                method: 'POST',
                data: {
                    'title': newTitle
                },
                success: function(response) {
                    if (response.success) {
                        $('#new-job-title').val('');
                        $('#addJobTitleModal').modal('hide');

                        // Call fetchOptions to update select options
                        fetchOptions();

                        // Show success alert
                        alert('Job title added successfully.');
                    } else {
                        alert('Failed to add job title:', response.message);
                    }
                },
                error: function(xhr, status, error) {
                    alert('An error occurred:', error);
                }
            });
        } else {
            console.error('Job title cannot be empty.');
        }
    });
});



// Pause video
document.addEventListener('DOMContentLoaded', function () {
    var player = document.getElementById('player');
    var modal = document.getElementById('shortReelModal');
    var closeModalBtn = modal ? modal.querySelector('.btn-close-custom') : null;

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function () {
            if (player && !player.paused) {
                player.pause();
            }
        });
    }
});


// Select Job Profile Type
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('jobseekerLink')) {
        document.getElementById('jobseekerLink').addEventListener('click', function(e) {
            e.preventDefault();
            if (!document.getElementById('jobseekerRadio').checked) {
                document.getElementById('jobseekerRadio').checked = true;
                toggleButtonStyle('jobseekerLink');
                deselectOther('employerLink');
            }
        });
    }

    if (document.getElementById('employerLink')) {
        document.getElementById('employerLink').addEventListener('click', function(e) {
            e.preventDefault();
            if (!document.getElementById('employerRadio').checked) {
                document.getElementById('employerRadio').checked = true;
                toggleButtonStyle('employerLink');
                deselectOther('jobseekerLink');
            }
        });
    }

    if (document.getElementById('continueBtn')) {
        document.getElementById('continueBtn').addEventListener('click', function() {
            var selectedType = document.querySelector('input[name="type"]:checked');
            if (selectedType) {
                document.getElementById('profileForm').submit();
            } else {
                alert('Please select a profile type.');
            }
        });
    }
});

function toggleButtonStyle(linkId) {
    var link = document.getElementById(linkId);
    if (link.classList.contains('btn-outline-custom')) {
        link.classList.remove('btn-outline-custom');
        link.classList.add('btn-custom');
    } else {
        link.classList.remove('btn-custom');
        link.classList.add('btn-outline-custom');
    }
}

function deselectOther(otherLinkId) {
    var otherLink = document.getElementById(otherLinkId);
    if (otherLink.classList.contains('btn-custom')) {
        otherLink.classList.remove('btn-custom');
        otherLink.classList.add('btn-outline-custom');
    }
}


// Multiple Image input field add class form-control
document.addEventListener('DOMContentLoaded', function() {
    var imageInput = document.getElementById('id_image');
    if (imageInput) {
        imageInput.classList.add('form-control');
    }
});



// video player
document.addEventListener('DOMContentLoaded', function() {
    var video = document.getElementById('player');
    var playpauseBtn = document.getElementById('playpause-btn');
    var volumeBar = document.getElementById('volume-bar');
    var progressBar = document.getElementById('progress-bar');
    var progressContainer = document.getElementById('progress-container');
    var backwardBtn = document.getElementById('backward-btn');
    var forwardBtn = document.getElementById('forward-btn');
    var currentTimeDisplay = document.getElementById('current-time');
    var totalDurationDisplay = document.getElementById('total-duration');
    var isDragging = false;

    // Function to safely add event listeners
    function addListener(element, event, handler) {
        if (element) {
            element.addEventListener(event, handler);
        }
    }

    if (video) {
        video.addEventListener('loadedmetadata', function() {
            // Set initial volume and progress bar width
            if (volumeBar) {
                volumeBar.value = video.volume;
            }
            if (progressBar) {
                progressBar.style.width = '0%';
            }

            // Display total duration
            if (totalDurationDisplay) {
                var totalDuration = formatTime(video.duration);
                totalDurationDisplay.textContent = totalDuration;
            }
        });

        video.addEventListener('timeupdate', function() {
            if (!isDragging && progressBar) {
                var percent = (video.currentTime / video.duration) * 100;
                progressBar.style.width = percent + '%';
            }

            // Display current time
            if (currentTimeDisplay) {
                var currentTime = formatTime(video.currentTime);
                currentTimeDisplay.textContent = currentTime;
            }
        });

        video.addEventListener('ended', function() {
            if (playpauseBtn) {
                playpauseBtn.innerHTML = '<i class="fa-regular fa-circle-play"></i>';
            }
        });
        // Disable right-click context menu on the video player
        video.addEventListener('contextmenu', function(e) {
            e.preventDefault();
        });
    }

    addListener(playpauseBtn, 'click', function() {
        if (video.paused || video.ended) {
            video.play();
            playpauseBtn.innerHTML = '<i class="fa-regular fa-circle-pause"></i>';
        } else {
            video.pause();
            playpauseBtn.innerHTML = '<i class="fa-regular fa-circle-play"></i>';
        }
    });

    addListener(volumeBar, 'input', function() {
        video.volume = volumeBar.value;
    });

    addListener(backwardBtn, 'click', function() {
        video.currentTime -= 10; // Jump backward 10 seconds
    });

    addListener(forwardBtn, 'click', function() {
        video.currentTime += 10; // Jump forward 10 seconds
    });

    addListener(progressContainer, 'mousedown', function(e) {
        isDragging = true;
        seek(e);
    });

    addListener(document, 'mousemove', function(e) {
        if (isDragging) {
            seek(e);
            if (progressContainer && currentTimeDisplay) {
                var rect = progressContainer.getBoundingClientRect();
                var offsetX = e.clientX - rect.left;
                var percent = Math.max(0, Math.min(1, offsetX / rect.width));
                var newTime = percent * video.duration;
                currentTimeDisplay.textContent = formatTime(newTime);
            }
        }
    });

    addListener(document, 'mouseup', function(e) {
        if (isDragging) {
            isDragging = false;
            seek(e);
        }
    });

    function seek(e) {
        if (progressContainer && progressBar) {
            var rect = progressContainer.getBoundingClientRect();
            var offsetX = e.clientX - rect.left;
            var percent = Math.max(0, Math.min(1, offsetX / rect.width));
            video.currentTime = percent * video.duration;
            progressBar.style.width = percent * 100 + '%';
        }
    }

    function formatTime(seconds) {
        var minutes = Math.floor(seconds / 60);
        var secs = Math.floor(seconds % 60);
        var millis = Math.floor((seconds % 1) * 1000);
        return (minutes < 10 ? '0' : '') + minutes + ':' + 
               (secs < 10 ? '0' : '') + secs + ':' + 
               (millis < 100 ? '0' : '') + (millis < 10 ? '0' : '') + millis;
    }
});

// Notification Count and mark as read
document.addEventListener('DOMContentLoaded', function() {
    function updateNotificationCount() {
        if (!notificationcountUrl) {
            return;
        }

        fetch(notificationcountUrl, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Update count for notificationButton
            const notificationCountElement1 = document.getElementById('notificationCount');
            if (notificationCountElement1) {
                if (data.unread_count === 0) {
                    notificationCountElement1.classList.add('d-none');
                } else {
                    notificationCountElement1.classList.remove('d-none');
                    notificationCountElement1.textContent = data.unread_count;
                }
            }

            // Update count for notificationButton2
            const notificationCountElement2 = document.getElementById('notificationCount2');
            if (notificationCountElement2) {
                if (data.unread_count === 0) {
                    notificationCountElement2.classList.add('d-none');
                } else {
                    notificationCountElement2.classList.remove('d-none');
                    notificationCountElement2.textContent = data.unread_count;
                }
            }
        })
        .catch(() => {
            // Handle errors silently without logging
        });
    }

    const notificationButtons = document.querySelectorAll('#notificationButton, #notificationButton2');
    notificationButtons.forEach(button => {
        if (button) {
            button.addEventListener('click', function() {
                updateNotificationCount();
            });
        }
    });

    // Initialize notification count on page load
    updateNotificationCount();

    // Auto-reload notification count every 10 seconds
    setInterval(updateNotificationCount, 10000);
});


// Load Notification
$(document).ready(function() {
    function loadNotifications() {
        // Show loading spinner
        $('#notificationList').html(`
            <div class="loading-spinner">
                <div class="lds-roller">
                    <div></div><div></div><div></div><div></div>
                    <div></div><div></div><div></div><div></div>
                </div>
            </div>
        `);

        $.ajax({
            url: notificationsUrl,
            method: 'GET',
            success: function(data) {
                // Sort notifications by creation date
                data.sort(function(a, b) {
                    return new Date(b.created) - new Date(a.created);
                });

                // Prepare the HTML for notifications
                let notificationsHtml = '';
                if (data.length > 0) {
                    data.forEach(notification => {
                        notificationsHtml += `
                            <a href="${notification.url}" class="list-group-item list-group-item-action d-flex flex-column flex-md-row gap-3 py-3" aria-current="true">
                                <div class="d-flex flex-grow-1 align-items-start">
                                    <img src="${notificationImage}" alt="notification" width="32" height="32" class="flex-shrink-0 me-3">
                                    <div class="d-flex flex-column w-100">
                                        <h6 class="mb-0">${notification.subject}</h6>
                                        <p class="mb-0 opacity-75">${notification.content}</p>
                                    </div>
                                </div>
                                <small class="opacity-50 text-nowrap mt-2 mt-md-0 align-self-md-center align-self-end">${moment(notification.created).fromNow()}</small>
                            </a>
                        `;
                    });
                }                
                else {
                    notificationsHtml = '<div class="no-notifications-container"><div class="no-notifications">No notifications</div></div>';
                }

                // Update the notification list with the fetched data
                $('#notificationList').html(notificationsHtml);
            },
            error: function() {
                $('#notificationList').html('<div class="error">Error loading notifications</div>');
            }
        });
    }

    $('#notificationModal').on('show.bs.modal', function () {
        loadNotifications();
    });
});