	.text
	.def	 @feat.00;
	.scl	3;
	.type	0;
	.endef
	.globl	@feat.00
.set @feat.00, 0
	.intel_syntax noprefix
	.file	"test"
	.def	 function_140001000;
	.scl	2;
	.type	32;
	.endef
	.globl	function_140001000              # -- Begin function function_140001000
	.p2align	4, 0x90
function_140001000:                     # @function_140001000
.seh_proc function_140001000
# %bb.0:                                # %dec_label_pc_140001000
	sub	rsp, 40
	.seh_stackalloc 40
	.seh_endprologue
	mov	ecx, 3
	call	function_140001070
	lea	ecx, [rax + 10]
	test	eax, eax
	mov	eax, 4294967295
	cmovne	rax, rcx
	add	rsp, 40
	ret
	.seh_endproc
                                        # -- End function
