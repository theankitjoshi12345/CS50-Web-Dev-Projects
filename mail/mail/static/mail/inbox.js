document.addEventListener('DOMContentLoaded', function() {

  // 1. Menu navigation event listeners
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // 2. ONE SINGLE listener attached to the entire document container body
  // This guarantees that even if we wipe #emails-view clean, the listener NEVER dies.
  document.body.addEventListener('click', (event) => {
    const target = event.target;

    // A. Clicked an Archive/Unarchive button
    if (target.classList.contains('archive-button')) {
      event.stopPropagation();

      const emailId = target.dataset.id;
      const shouldArchive = target.dataset.action === 'archive';

      fetch(`/emails/${emailId}`, {
        method: 'PUT',
        body: JSON.stringify({ archived: shouldArchive })
      })
      .then(() => {
        setTimeout(() => {
          load_mailbox('inbox');
        }, 100);
      });
      return;
    } 

    else if (target.id === 'reply-button'){
      event.stopPropagation();

      document.querySelector('#emails-view').style.display = 'none';
      const composeView = document.querySelector('#compose-view');
      composeView.style.display = 'block';
      const recipients = document.querySelector('#compose-recipients');
      const subject = document.querySelector('#compose-subject');
      const body = document.querySelector('#compose-body');

      const id = target.dataset.id;

      fetch(`emails/${id}`)
      .then(response => response.json())
      .then(data => {
        recipients.value = `${data.sender}`;
        subject.value = `Re: ${data.subject}`;
        body.value = `On ${data.timestamp}, ${data.sender} wrote: ${data.body} \n`;

      })





    }

    // B. Clicked anywhere inside an email row container
    else if (target.closest('.individual-email-div')) {
      const emailDiv = target.closest('.individual-email-div');
      const emailId = emailDiv.dataset.id;
      load_email(emailId);
      return
    }
  
  });

  // 3. Compose email form handling
  document.querySelector('#compose-form').onsubmit = () => {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        subject: subject,
        body: body,
        recipients: recipients
      })
    })
    .then(async response => {
        if (!response.ok){
          const errData = await response.json();
          return Promise.reject(errData.error);
        }
        return response.json()
    })
    .then((result) => {
      console.log(result);
      load_mailbox("sent");
    })
    .catch(error => {
        console.log(error);

        const composeView = document.querySelector('#compose-view');
        
        const oldAlert = composeView.querySelector('.alert');
        if (oldAlert) oldAlert.remove();

        const alertDiv = document.createElement('div');
        alertDiv.className = "alert alert-danger m-2";

        alertDiv.innerHTML = error;
        composeView.prepend(alertDiv);
    });
    return false;
  };

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  const emailView = document.querySelector('#emails-view');
  const composeView = document.querySelector('#compose-view');

  emailView.style.display = 'none'; 
  composeView.style.display = 'block'; 

  const oldAlert = composeView.querySelector(".alert");
  if (oldAlert){
    oldAlert.remove();
  }

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  const emailsView = document.querySelector('#emails-view');
  
  emailsView.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none'; 

  // Reset the view title and dump old rows safely
  emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status:${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    data.forEach(email => {
      const emailDiv = document.createElement('div');
      emailDiv.className = "individual-email-div";
      emailDiv.dataset.id = email.id;
      
      emailDiv.innerHTML = `<b>${email.sender}</b> - ${email.subject} <br> <small>${email.timestamp}</small>`;
      
      // Add background color depending on read status (CS50W specification requirement!)
        if (email.read) {
        // A clean, distinct light gray for read emails
        emailDiv.style.backgroundColor = '#d6d6d6'; 
        } else {
        // A solid white for unread emails (Notice: no hashtag before the word 'white'!)
        emailDiv.style.backgroundColor = 'white'; 
        }

      if (mailbox.toLowerCase() === "inbox") {
        const button = document.createElement('button');
        button.className = "archive-button float-right";
        button.innerHTML = "Archive";
        button.dataset.id = email.id;
        button.dataset.action = "archive";
        emailDiv.append(button);

      } else if (mailbox.toLowerCase() === "archive") {
        const button = document.createElement('button');
        button.className = "archive-button float-right";
        button.innerHTML = "Unarchive";
        button.dataset.id = email.id;
        button.dataset.action = "unarchive";
        emailDiv.append(button);
      }

      emailsView.append(emailDiv);
    });
  })
  .catch(error => console.log(`Fetch error: ${error}`));
}

function load_email(id) {
  fetch(`/emails/${id}`)
  .then(response => {
    return response.json();
  })
  .then(email => {
    const emailsView = document.querySelector('#emails-view');
    document.querySelector('#compose-view').style.display = 'none';
    emailsView.style.display = 'block';
    
    // Wipe layout clean to build individual visualization frame
    emailsView.innerHTML = '';

    const individualEmail = document.createElement('div');
    individualEmail.className = "individual-email p-3";
    
    individualEmail.innerHTML = `
      <div><strong>From:</strong> ${email.sender}</div>
      <div><strong>To:</strong> ${email.recipients.join(', ')}</div>
      <div><strong>Subject:</strong> ${email.subject}</div>
      <div><strong>Timestamp:</strong> ${email.timestamp}</div>
      <hr>
      <div style="white-space: pre-wrap;">${email.body}</div>
      <hr>
      <button id="reply-button" data-id="${email.id}" class="btn btn-sm btn-outline-primary"> ⤵ Reply </button>
    `;

    emailsView.append(individualEmail);

    // Mark the email as read since we just opened it!
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ read: true })
    });
  })
  .catch(error => {
    // THIS IS YOUR SAFETY NET
    console.log(`Email load error: ${error}`);
  })
}
