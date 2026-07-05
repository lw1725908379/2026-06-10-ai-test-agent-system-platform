FROM node:22

RUN apt-get update -qq && apt-get install -y -qq socat >/dev/null 2>&1

RUN npm install -g gitnexus@latest --ignore-scripts

ENV npm_config_ignore_scripts=false
RUN node /usr/local/lib/node_modules/gitnexus/node_modules/@ladybugdb/core/install.js 2>&1 | tail -3
ENV npm_config_ignore_scripts=true

EXPOSE 4747

CMD ["sh", "-c", "cd /repo && socat TCP-LISTEN:4747,fork,reuseaddr TCP6:[::1]:4748 & exec gitnexus serve --port 4748"]
