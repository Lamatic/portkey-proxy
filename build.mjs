import fs from "fs";

function load_toml(path) {
    return fs.readFileSync(path, "utf8");
}

function add_custom_domain(config, custom_domain) {
    const baseText = `compatibility_flags = [ "nodejs_compat" ]`;
    const customDomainText = `${baseText}\nroutes = [ { pattern = "${custom_domain}", custom_domain = true } ]`;
    return config.replace(baseText, customDomainText);
}

function update_service_name(config, service_name, custom_domain) {
    // const updated_config = config.replace("rubeus", service_name);
    const regex = new RegExp("rubeus", 'g');
const updated_config = config.replace(regex, service_name);
    if (custom_domain) {
        return add_custom_domain(updated_config, custom_domain);
    }
    return updated_config;
}

function build() {
    const base_wrangler_config = load_toml("./wrangler.toml");
    const custom_domain = process.env.CUSTOM_DOMAIN;
    const service_name = process.env.SERVICE_NAME;

    if (!service_name) {
        throw new Error("SERVICE_NAME must be set");
    }

    const wrangler_config = update_service_name(base_wrangler_config, service_name, custom_domain);
    fs.writeFileSync("wrangler.toml", wrangler_config);
}

build();