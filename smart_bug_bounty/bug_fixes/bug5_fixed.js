async function fetchUserMetrics(userIds, fetchMock) {
    if (!Array.isArray(userIds) || userIds.length === 0) {
        return [];
    }
    return Promise.all(userIds.map(id => fetchMock(id)));
}

const mockApi = (id) => new Promise(resolve => setTimeout(() => resolve({ id, score: id * 10 }), 10));

fetchUserMetrics([1, 2, 3], mockApi).then(data => {
    console.log("Fetched metrics count:", data.length);
});
