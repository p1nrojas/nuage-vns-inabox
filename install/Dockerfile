FROM centos:latest

# Install all packages
RUN yum -y install epel-release && yum clean all
RUN yum -y install python-pip && yum clean all
RUN yum -y install ansible && yum clean all
RUN yum -y install vim && yum clean all
RUN yum -y install curl && yum clean all
RUN yum -y install git && yum clean all

# install sdk from nuage
RUN pip install --upgrade pip
RUN pip install vspk
RUN pip install pexpect

# Generate user dev and his files
RUN useradd dev
WORKDIR /home/dev
ENV HOME /home/dev
ADD vimrc /home/dev/.vimrc
ADD bash_profile /home/dev/.bash_profile
RUN mkdir -p /home/dev/.vim/autoload /home/dev/.vim/bundle
RUN curl -LSso /home/dev/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
RUN git clone git://github.com/chase/vim-ansible-yaml.git  /home/dev/.vim/bundle/vim-ansible-yaml
RUN git clone https://github.com/lepture/vim-jinja.git /home/dev/.vim/bundle/vim-jinja

RUN chown -R dev: /home/dev
USER dev
