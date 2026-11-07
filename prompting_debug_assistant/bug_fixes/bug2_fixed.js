function processUserTransactions(transactions) {
    const summary = {
        totalCredits: 0,
        totalDebits: 0,
        transactionCount: transactions.length
    };

    transactions.forEach(tx => {
        if (!tx || !tx.details || !tx.details.amount) {
            return;
        }

        const amount = parseFloat(tx.details.amount);
        if (isNaN(amount)) {
            return;
        }

        if (tx.type.toLowerCase() === "credit") {
            summary.totalCredits += amount;
        } else if (tx.type.toLowerCase() === "debit") {
            summary.totalDebits += amount;
        }
    });

    summary.totalCredits = Number(summary.totalCredits.toFixed(2));
    summary.totalDebits = Number(summary.totalDebits.toFixed(2));
    summary.netBalance = Number((summary.totalCredits - summary.totalDebits).toFixed(2));
    return summary;
}

const batch = [
    { type: "credit", details: { amount: "150.50" } },
    { type: "debit", details: null },
    { type: "credit", details: { amount: "89.20" } }
];

const result = processUserTransactions(batch);
console.log(result);
