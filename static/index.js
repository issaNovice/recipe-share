document.addEventListener('DOMContentLoaded', () => {
    const viewButtons = document.querySelectorAll('.view-button');
    const modal = document.getElementById('lightbox-modal');
    const closeButton = document.querySelector('.close-button');
    const meepBody = document.getElementById('meep-body');
    const meepIngredients = document.getElementById('meep-ingredients');
    const meepProcedure = document.getElementById('meep-procedure');

    viewButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            const meepId = e.target.getAttribute('data-id');
            const response = await fetch(`/meep_show/${meepId}`);
            const data = await response.json();

            meepBody.innerHTML = data.body.replace(/\n/g, '<br>');
            meepIngredients.innerHTML = `<strong>Ingredients:</strong><br>${data.ingredients.replace(/\n/g, '<br>')}`;
            meepProcedure.innerHTML = `<strong>Procedure:</strong><br>${data.procedure.replace(/\n/g, '<br>')}`;
            
            modal.style.display = 'block';
        });
    });

    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target == modal) {
            modal.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const extraNav = document.getElementById('extra-nav');
    const dropupMenu = extraNav.querySelector('.dropup-menu');
    const menuLinks = dropupMenu.querySelectorAll('a');

    extraNav.querySelector('.hi').addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation(); 
        dropupMenu.style.display = dropupMenu.style.display === 'block' ? 'none' : 'block';
    });

    menuLinks.forEach(link => {
        link.addEventListener('click', function() {
            dropupMenu.style.display = 'none';
        });
    });

    document.addEventListener('click', function(event) {
        if (!extraNav.contains(event.target)) {
            dropupMenu.style.display = 'none';
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var lazyloadImages = document.querySelectorAll(".lazy");

    function lazyload() {
        lazyloadImages.forEach(function(img) {
            if (img.getBoundingClientRect().top < window.innerHeight && img.getBoundingClientRect().bottom >= 0 && getComputedStyle(img).display !== "none") {
                img.src = img.dataset.src;
                img.classList.remove("lazy");
            }
        });
    }

    lazyload();

    window.addEventListener("scroll", lazyload);
});
