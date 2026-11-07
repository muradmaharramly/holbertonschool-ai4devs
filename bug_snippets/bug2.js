function processUserTransactions(transactions) {
    const summary = {
        totalCredits: 0,
        totalDebits: 0,
        transactionCount: transactions.length
    };

    transactions.forEach(tx => {
        const amount = parseFloat(tx.details.amount);
        if (tx.type.toLowerCase() === "credit") {
            summary.totalCredits += amount;
        } else if (tx.type.toLowerCase() === "debit") {
            summary.totalDebits += amount;
        }
    });

    summary.netBalance = summary.totalCredits - summary.totalDebits;
    return summary;
}

const batch = [
    { type: "credit", details: { amount: "150.50" } },
    { type: "debit", details: null },
    { type: "credit", details: { amount: "89.20" } }
];

const result = processUserTransactions(batch);
console.log(result);
