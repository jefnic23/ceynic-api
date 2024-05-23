<nav>
    <a href="/">Home</a>
    <a href="/browse">Browse art</a>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
</nav>

<slot></slot>

<style>
    nav {
        min-height: 50px;
        background-color: #f8f8f8;
        border: 1px solid #e7e7e7;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    nav a {
        text-transform: uppercase;
        text-decoration: none;
        margin: 0 0.5rem;
        color: rgba(0, 0, 0, .55);
        font-size: 13px;
        font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
</style>