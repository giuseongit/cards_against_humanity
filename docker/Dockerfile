FROM ruby:3-buster


RUN apt-get update
RUN apt-get install -y\
    apt-utils\
    postgresql\
    redis

RUN echo "\
function parse_git_branch {\n\
    local branch=\$(git branch --show-current 2>/dev/null)                   \n\
    [[ \${branch} == '' ]] && exit                                           \n\
    local st=\$(git status --short --untracked-files=no | wc -l)             \n\
    local hash=\$(git show --format=%h --no-patch)                           \n\
                                                                             \n\
    echo -n \"(git::\${branch} \${hash}\"                                    \n\
    [[ \${st} != 0 ]] && echo -n ' !'                                        \n\
    echo ')'                                                                 \n\
}                                                                            \n\
LIGHT_RED=\"\\e[1;31m\"                                                      \n\
LIGHT_BLUE=\"\\e[1;34m\"                                                     \n\
YELLOW=\"\\e[1;33m\"                                                         \n\
RESET_COLOR=\"\\e[0m\"                                                       \n\
                                                                             \n\
export PS1=\"(\${LIGHT_RED}root@app\${RESET_COLOR}):\${LIGHT_BLUE}\w\${YELLOW}\\\$(parse_git_branch)\${RESET_COLOR}$ \"\n\
                                                                             \n\
/etc/init.d/postgresql status > /dev/null                                    \n\
pg_status=\$?                                                                \n\
if [[ \${pg_status} != 0 ]]; then                                            \n\
    /etc/init.d/postgresql start &> /dev/null                                \n\
fi                                                                           \n\
/etc/init.d/redis-server status > /dev/null                                  \n\
redis_status=\$?                                                             \n\
if [[ \${redis_status} != 0 ]]; then                                         \n\
    /etc/init.d/redis-server start &> /dev/null                              \n\
fi                                                                           \n\
" >> /root/.bashrc

RUN /etc/init.d/postgresql start && su -c "createuser -d root && createdb root" postgres

# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ENV NVM_DIR /usr/local/nvm
RUN mkdir $NVM_DIR

# Install nvm with node and npm
RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.38.0/install.sh | bash \
    && source $NVM_DIR/nvm.sh \
    && nvm install --lts \
    && nvm use default \
    && npm install --global yarn

RUN gem install bundler
RUN gem install sidekiq
RUN gem install foreman

WORKDIR /app
