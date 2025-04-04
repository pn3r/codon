o
    ���g_  �                   @   s�  d dl Z d dlZd dlZd dlZd dlZd dlmZmZ d dlmZm	Z	m
Z
mZmZmZ d dlmZ d dlmZ d dlmZ d dlmZ d dlmZ e�  e��  e�d	�Ze�d
�Ze�d�Zee�Ze�dd�e_eee�ee�Z dd� Z!e �"� Z#e#�$e!� � eeed�Z%i Z&dd� Z'dd� Z(dd� Z)e�*d�dd� �Z+ej*ddgd�dd� �Z,ej*ddgd�d d!� �Z-e�*d"�d#d$� �Z.ej*d%dgd�d&d'� �Z/ed(kr�ej0d)d*� dS dS )+�    N)�datetime�	timedelta)�Flask�render_template�request�jsonify�	send_file�session)�Limiter)�get_remote_address)�TelegramClient)�StringSession)�load_dotenvZAPI_IDZAPI_HASHZCRPXZFLASK_SECRET_KEYZdefault_secret_keyc                   �   s   �t �� I d H  d S )N)�client�start� r   r   �ppy.py�sc   s   �r   )�appc                 �   s,   �t jd| |� d|� �d�I d H }|j|fS )N�me� | )�fileZcaption)r   r   �id)Zfb�fn�p�mr   r   r   �stt   s   � 
r   c                  �   sr   �t jddd�I d H i } }| D ]&}|jr6|jr6|j�dd�}t|�dkr6|j|�|d �� i �|d �� < q|S )Nr   �d   )�limitr   �   �   r   )	r   �get_messagesr   �text�split�lenr   �
setdefault�strip)r   �pm�xr   r   r   r   �fuf#   s   �.�r)   c                 �   s*   �t jd| d�I d H }t j|td�I d H S )Nr   )Zids)r   )r   r!   Zdownload_media�bytes)�ir   r   r   r   �dft+   s   �r,   �/c                   C   s   t d�S )Nz
index.html)r   r   r   r   r   r+   /   s   r+   z/uploadZPOST)�methodsc                  C   st   t j�d�t�d�i } }}| stddd��dfS | D ]}t�t|�	� |j
|��d ||j
< qtd||d	��d
fS )N�files�   �errorzNo files provided��status�messagei�  r   �success)r3   Zuploaded_files�password��   )r   r/   Zgetlist�secretsZtoken_urlsafer   �loop�run_until_completer   �read�filename)�fr   �rr(   r   r   r   �u2   s   ,r?   z/verify_passwordc                  C   s�   t � t�� tj�d�} }}| tv r#t|  d |tdd� k r#t| = | tv r8t|  d dkr8tddd	��d
fS t	�
t� �}||v rW|td< t�| d � td|| d��dfS | tv rft|  d d |d�nd|d�t| < tddd	��dfS )Nr6   �timer   )Zminutes�count�   r1   zToo many failed attemptsr2   i�  �authorized_passwordr5   )r3   r/   r7   )rA   r@   zInvalid password�  )r   r   �nowr   Zjson�get�FAr   r   r9   r:   r)   r	   �pop)ZiprE   �pwr'   r   r   r   �vp9   s   (*,rJ   z/download/<fn>c                 C   s\   t �d�}|s	dS t�t� �}||vs| || vrdS tt�t�t|| |  ���d| d�S )NrC   )�UnauthorizedrD   T)Zas_attachmentZdownload_name)	r	   rF   r9   r:   r)   r   �io�BytesIOr,   )r   rI   r'   r   r   r   �dF   s
   
&rN   z/delete/<fn>c                    sp   t �� �d��t�t� ���r��vs� �� vr"tddd��dfS � ��fdd�}t�|� � tdd	i�d
fS )Nr6   r1   rK   r2   rD   c                   �   s"   �t �d�� �  g�I d H  d S )Nr   )r   Zdelete_messagesr   �r   r   r'   r   r   �adS   s   �  zdf.<locals>.adr3   r5   r7   )r   Zget_jsonrF   r9   r:   r)   r   )r   rP   r   rO   r   �dfN   s   *rQ   �__main__F)�debug)1ZasynciorL   Znest_asyncior8   �osr   r   Zflaskr   r   r   r   r   r	   Zflask_limiterr
   Zflask_limiter.utilr   Ztelethon.syncr   Ztelethon.sessionsr   Zdotenvr   Zapply�getenv�A�B�S�__name__r   Z
secret_keyr   r   Zget_event_loopr9   r:   ZlimiterrG   r   r)   r,   Zrouter+   r?   rJ   rN   rQ   �runr   r   r   r   �<module>   sR     







�