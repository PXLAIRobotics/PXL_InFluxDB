FROM ubuntu:22.04

# We love UTF!
ENV LANG C.UTF-8

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install some handy tools.
RUN set -x \
    && apt-get update \
    && apt-get --with-new-pkgs upgrade -y \
    && apt-get install -y iputils-ping \ 
    && apt-get install -y apt-transport-https ca-certificates \
    && apt-get install -y python3-pip exuberant-ctags \
    && apt-get install -y git vim tmux nano htop sudo curl wget gnupg2 \
    && apt-get install -y bash-completion \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -ms /bin/bash user \
    && echo "user:user" | chpasswd && adduser user sudo \
    && echo "user ALL=(ALL) NOPASSWD: ALL " >> /etc/sudoers

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN set -x \
    && pip3 install powerline-shell \
    && pip3 install uvicorn[standard]==0.15.0 gunicorn==20.1.0 fastapi==0.68.1 \
    && pip3 install influxdb==5.3.1 pytest==7.1.2 \
    && pip3 install pandas==2.2.3 \
    && pip3 install pymongo==4.2.0 \
    && pip3 install pyjwt==2.4.0 \
    && pip3 install bcrypt==4.0.0 \
    && pip3 install passlib==1.7.4 \
    && pip3 install slowapi==0.1.6

RUN set -x \
    && apt-get update \
    && apt-get install -y openssh-server \
    && apt-get install net-tools \
    && rm -rf /var/lib/apt/lists/*

USER user
WORKDIR /home/user

RUN git clone https://github.com/jimeh/tmux-themepack.git ~/.tmux-themepack  \
        && git clone https://github.com/tmux-plugins/tmux-resurrect ~/.tmux-resurrect
COPY --chown=user:user ./.tmux.conf /home/user/.tmux.conf
COPY --chown=user:user ./.powerline.sh /home/user/.powerline.sh

# Set some decent colors if the container needs to be accessed via /bin/bash.
RUN echo LS_COLORS=$LS_COLORS:\'di=1\;34:ln=36\' >> ~/.bashrc \
        && echo export LS_COLORS >> ~/.bashrc \
        && echo 'source ~/.powerline.sh' >> ~/.bashrc \
        && echo 'alias tmux="tmux -2"' >> ~/.bashrc \
        && echo 'PATH=~/bin:$PATH' >> ~/.bashrc \
        && touch ~/.sudo_as_admin_successful # To surpress the sudo message at run.

STOPSIGNAL SIGTERM
CMD sudo service ssh start && /bin/bash
