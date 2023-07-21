function Worker(
    id, phone,
    firstName, secondName,
) {
    this.id = id;
    this.phone = phone;
    this.firstName = firstName;
    this.secondName = secondName;
}

Worker.prototype.fullName = function() {
    return `${this.firstName} ${this.secondName}`
}

Worker.prototype.creatLink = function() {
    const currentURL = new URL(window.location.href);
    const pathName = `/users/${this.id}`
    return (new URL(`${currentURL.origin}${pathName}`)).href
}


Worker.fromOblect = (__object) => {
    return new Worker(
        __object.id,
        __object.phone,
        __object.first_name,
        __object.second_name
    )
}