async function fetchUserMetrics(userIds, fetchMock) {
    const results = [];
    userIds.forEach(async (id) => {
        const data = await fetchMock(id);
        results.push(data);
    });
    return results;
}

const mockApi = (id) => new Promise(resolve => setTimeout(() => resolve({ id, score: id * 10 }), 10));

fetchUserMetrics([1, 2, 3], mockApi).then(data => {
    console.log("Fetched metrics count:", data.length);
});
