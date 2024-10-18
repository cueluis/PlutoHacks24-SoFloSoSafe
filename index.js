const { OpenAI } = require('openai');

const openai = new OpenAI({ apiKey: ''});

async function runCompletion () {
    const chatCompletion = await openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [{"role": "user", "content": "Hello!"}],
    });

    console.log(completion.data.choices[0].text);
}

runCompletion();