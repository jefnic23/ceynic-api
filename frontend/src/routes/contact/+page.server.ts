import type { Actions } from "@sveltejs/kit";

export const actions = {
    default: async ({ request }) => {
        const formData = await request.formData();

        const response = await fetch("http://127.0.0.1:8000/contact", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            console.log("Error submitting form.");
        }
    }
} satisfies Actions;