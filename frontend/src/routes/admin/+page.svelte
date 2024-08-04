<script lang="ts">
    import Modal from "$lib/components/Modal.svelte";

    let showModal: boolean = true;
</script>

<Modal bind:showModal showClose={false}>
    <h2 slot="header">
        Login
    </h2>
    <form>
        <label for="email">Email</label>
        <input id="email" name="email" value="" placeholder="Your email..." required />
        <label for="password">Email</label>
        <input id="password" name="password" value="" placeholder="Your password..." required />
        <button>Submit</button>
    </form>
</Modal>