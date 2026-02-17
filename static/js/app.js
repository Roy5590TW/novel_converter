const views = {
    home: document.getElementById('view-home'),
    chapters: document.getElementById('view-chapters'),
    read: document.getElementById('view-read')
};

let activeBook = "";
let currentChNum = 1;
let totalChapters = 0;

// Page switching logic
export function switchView(viewName) {
    Object.values(views).forEach(v => v.classList.add('hidden'));
    views[viewName].classList.remove('hidden');
    window.scrollTo(0, 0);
}

export function showHome() { switchView('home'); }
export function showChapters() { 
    switchView('chapters'); 
    
    requestAnimationFrame(() => {
        setTimeout(() => {
            if (currentChNum) {
                const targetEl = document.querySelector(`#chapter-list li[data-chnum="${currentChNum}"]`);
                
                if (targetEl) {
                    targetEl.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });

                    targetEl.classList.add('highlight-active');
                    setTimeout(() => targetEl.classList.remove('highlight-active'), 1500);
                }
            }
        }, 10);
    });
}

// Initialization: Fetch all books
export async function initLibrary() {
    try {
        const res = await fetch('/api/books');
        if (!res.ok) throw new Error("無法取得書籍列表");
        
        const books = await res.json();
        const list = document.getElementById('book-list');

        list.innerHTML = books.map(book => `
            <li data-bookname="${book.book_name}">
                <div class="book-info">
                    <span class="icon">📖</span>
                    <span class="title">${book.book_name}</span>
                    <span class="author">${book.author}</span>
                </div>
            </li>
        `).join('');

        list.onclick = (e) => {
            const li = e.target.closest('li');
            if (li && li.dataset.bookname) {
                loadChapters(li.dataset.bookname);
            }
        };
    } catch (err) {
        console.error("Failed to load library:", err);
    }
}

// book metadata
function renderMetadata(metadata) {
    document.getElementById('info-author').innerText = metadata.author || '未知';
    document.getElementById('info-status').innerText = metadata.status || '連載中';
    document.getElementById('info-description').innerText = metadata.description || '暫無簡介';
    
    const tagsContainer = document.getElementById('info-tags');
    if (metadata.tags) {
        tagsContainer.innerHTML = metadata.tags.split(',')
            .map(tag => `<span class="tag-badge">${tag.trim()}</span>`)
            .join(' ');
    } else {
        tagsContainer.innerText = '無';
    }
}


// Click on the book: retrieve chapters
export async function loadChapters(bookName) {
    activeBook = bookName;
    document.getElementById('current-book-name').innerText = bookName;

    try {
        const [resChapters, resMeta] = await Promise.all([
            fetch(`/api/chapters/${encodeURIComponent(bookName)}`),
            fetch(`/api/metadata/${encodeURIComponent(bookName)}`)
        ]);

        if (!resChapters.ok) throw new Error("Chapters not found");
        
        const chapters = await resChapters.json();
        totalChapters = chapters.length;

        const list = document.getElementById('chapter-list');
        list.innerHTML = chapters.map(ch => 
            `<li data-chnum="${ch.chapter_num}">${ch.title}</li>`
        ).join('');

        list.onclick = (e) => {
            const li = e.target.closest('li');
            if (li && li.dataset.chnum) {
                loadContent(parseInt(li.dataset.chnum));
            }
        };

        if (resMeta.ok) {
            const metadata = await resMeta.json();
            renderMetadata(metadata);
        }

        switchView('chapters');
        
    } catch (err) {
        console.error(err);
        alert("載入失敗: " + err.message);
    }
}

// Click on the chapter: Fetch Content
export async function loadContent(chNum) {
    currentChNum = chNum;
    try {
        const res = await fetch(`/api/content/${encodeURIComponent(activeBook)}/${chNum}`);
        if (!res.ok) return;

        const data = await res.json();
        
        document.getElementById('current-chapter-title').innerText = data.title;
        document.getElementById('content-area').innerText = data.content;
        
        document.getElementById('prev-btn').disabled = (currentChNum <= 1);
        document.getElementById('next-btn').disabled = (currentChNum >= totalChapters);

        switchView('read');
    } catch (err) {
        console.error("Error loading content:", err);
    }
}
export function prevChapter() { if (currentChNum > 1) loadContent(currentChNum - 1); }
export function nextChapter() { if (currentChNum < totalChapters) loadContent(currentChNum + 1); }