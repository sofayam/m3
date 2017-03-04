; wrapper for python xmlrpc call to reload a capsule in the capsule editor
; bound to key M-r
; port defaults to 6666 - to set to any other value use prefix argument (C-u <port-value>)

(provide 'reload)

(defvar reload-port "6666" "Port used by the xmlrpc server of the capsule editor")

(defun reload-capsule (&optional port)
  (interactive "p")


  (if (string= mode-name "Modula 3")                                 ; only do any of this if we are in modula-3 mode

      (progn 
	(if (> port 1)                                               ; deal with prefix argument
	    (progn
	      (setq reload-port (int-to-string port))))



	(save-buffer)

        ;; maybe try compiling it

	(start-process "reload-process"   
		       "*reload*"                                    ; buffer for diagnostic info 
		       "python"                                      ; a language with a decent xmlrpc lib
		       (concat (getenv "M3_HOME") "/bin/reload.py")  ; construct the path to our reload script
		       reload-port                                   ; the eternally changing port
		       (buffer-name))                                ; name of current buffer will be used to derive capsule name
	)))

(global-set-key "\M-r" 'reload-capsule)