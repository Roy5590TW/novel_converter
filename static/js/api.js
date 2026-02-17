
export async function getBooks() {
    const res = await fetch('/api/books');
    if (!res.ok) throw new Error("無法取得書籍列表");
    return await res.json();
}

export async function getBookDetails(bookName) {
    const name = encodeURIComponent(bookName);
    const [resChapters, resMeta] = await Promise.all([
        fetch(`/api/chapters/${name}`),
        fetch(`/api/metadata/${name}`)
    ]);
    if (!resChapters.ok) throw new Error("Chapters not found");
    
    return {
        chapters: await resChapters.json(),
        metadata: resMeta.ok ? await resMeta.json() : null
    };
}

export async function getChapterContent(activeBook, chNum) {
    const res = await fetch(`/api/content/${encodeURIComponent(activeBook)}/${chNum}`);
    if (!res.ok) throw new Error("Content not found");
    return await res.json();
}